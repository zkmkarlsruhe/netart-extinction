#!/usr/bin/env python3
"""
Probe canonical URLs from the unified net art corpus.

This script is non-destructive:
- reads data/corpus/netart-corpus.json
- writes separate probe outputs to data/corpus/

Outputs:
- data/corpus/url-probe-results.json
- data/corpus/url-probe-summary.json
"""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests


ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "data" / "corpus" / "netart-corpus.json"
RESULTS_PATH = ROOT / "data" / "corpus" / "url-probe-results.json"
SUMMARY_PATH = ROOT / "data" / "corpus" / "url-probe-summary.json"

USER_AGENT = "Mozilla/5.0 (compatible; netart-extinction-probe/1.0)"
TIMEOUT = 12
MAX_REDIRECTS = 10


def classify_probe(result: dict[str, Any]) -> str:
    error = result.get("error_type")
    status_code = result.get("status_code")
    final_url = result.get("final_url", "")
    redirected = result.get("redirected", False)

    if error == "timeout":
        return "timeout"
    if error in {"dns", "connection", "ssl", "request", "too_many_redirects"}:
        return "unreachable"
    if status_code is None:
        return "unknown"
    if 200 <= status_code < 300:
        if redirected and final_url and final_url != result.get("url"):
            return "live-redirect"
        return "live"
    if status_code in {401, 403}:
        return "blocked"
    if status_code == 404:
        return "missing"
    if 400 <= status_code < 500:
        return "client-error"
    if 500 <= status_code < 600:
        return "server-error"
    return "other"


def evidence_flags(result: dict[str, Any]) -> list[str]:
    flags = []
    outcome = result["outcome"]
    final_url = result.get("final_url", "")
    host = result.get("final_host", "")

    if outcome in {"missing", "unreachable", "timeout"}:
        flags.append("url-not-working")
    if outcome == "blocked":
        flags.append("access-blocked")
    if outcome == "live-redirect":
        flags.append("redirected")
    if final_url.startswith("https://webcache.googleusercontent.com"):
        flags.append("cached-copy")
    if "web.archive.org" in host or "archive.org" in host:
        flags.append("archive-host")
    return flags


def probe_url(corpus_row: dict[str, Any]) -> dict[str, Any]:
    url = corpus_row["canonical_url"]
    parsed = urlparse(url)
    result: dict[str, Any] = {
        "corpus_id": corpus_row["corpus_id"],
        "title": corpus_row["title"],
        "artist": corpus_row["artist"],
        "url": url,
        "host": parsed.netloc.lower(),
        "started_at": int(time.time()),
        "status_code": None,
        "final_url": "",
        "final_host": "",
        "content_type": "",
        "content_length": None,
        "redirected": False,
        "history": [],
        "error_type": "",
        "error": "",
    }

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    session.max_redirects = MAX_REDIRECTS

    try:
        response = session.get(
            url,
            timeout=TIMEOUT,
            allow_redirects=True,
            stream=True,
        )
        result["status_code"] = response.status_code
        result["final_url"] = response.url
        result["final_host"] = urlparse(response.url).netloc.lower()
        result["content_type"] = response.headers.get("content-type", "")
        result["content_length"] = response.headers.get("content-length")
        result["history"] = [
            {
                "status_code": hop.status_code,
                "url": hop.url,
            }
            for hop in response.history
        ]
        result["redirected"] = bool(response.history)
        response.close()
    except requests.exceptions.TooManyRedirects as exc:
        result["error_type"] = "too_many_redirects"
        result["error"] = str(exc)
    except requests.exceptions.Timeout as exc:
        result["error_type"] = "timeout"
        result["error"] = str(exc)
    except requests.exceptions.SSLError as exc:
        result["error_type"] = "ssl"
        result["error"] = str(exc)
    except requests.exceptions.ConnectionError as exc:
        message = str(exc).lower()
        if "name or service not known" in message or "failed to resolve" in message or "nodename nor servname" in message:
            result["error_type"] = "dns"
        else:
            result["error_type"] = "connection"
        result["error"] = str(exc)
    except requests.exceptions.RequestException as exc:
        result["error_type"] = "request"
        result["error"] = str(exc)

    result["finished_at"] = int(time.time())
    result["outcome"] = classify_probe(result)
    result["evidence_flags"] = evidence_flags(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Only probe the first N URLs")
    parser.add_argument("--workers", type=int, default=16, help="Concurrent worker count")
    args = parser.parse_args()

    corpus = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))
    targets = [row for row in corpus if row.get("canonical_url")]
    if args.limit > 0:
        targets = targets[: args.limit]

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(probe_url, row) for row in targets]
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda row: row["corpus_id"])

    outcome_counts = Counter(row["outcome"] for row in results)
    flag_counts = Counter(flag for row in results for flag in row["evidence_flags"])
    host_counts = Counter(row["host"] for row in results if row["host"])

    summary = {
        "probed_records": len(results),
        "outcomes": dict(sorted(outcome_counts.items())),
        "evidence_flags": dict(sorted(flag_counts.items())),
        "top_hosts": host_counts.most_common(50),
        "generated_at": int(time.time()),
    }

    RESULTS_PATH.write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    SUMMARY_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
