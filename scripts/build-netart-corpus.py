#!/usr/bin/env python3
"""
Build a unified net art corpus from data/sources/*/artworks.json without
modifying any source-specific datasets.

Outputs:
- data/corpus/netart-corpus.json
- data/corpus/extinction-matching-queue.json
- data/corpus/source-stats.json
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "data" / "sources"
CORPUS_DIR = ROOT / "data" / "corpus"


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_text(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"^[\"'`]+|[\"'`]+$", "", value)
    return value


def normalize_title(value: str) -> str:
    value = normalize_text(value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def normalize_artist(value: str) -> str:
    value = normalize_text(value)
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def normalize_url(value: str) -> str:
    if not value:
        return ""
    value = value.strip()
    if not re.match(r"^https?://", value, re.I):
        value = "http://" + value
    try:
        parsed = urlparse(value)
    except Exception:
        return value.lower().rstrip("/")
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/+", "/", parsed.path or "/").rstrip("/")
    if not path:
        path = "/"
    query = f"?{parsed.query}" if parsed.query else ""
    return f"{parsed.scheme.lower()}://{host}{path}{query}"


def url_host(value: str) -> str:
    if not value:
        return ""
    try:
        parsed = urlparse(value)
        host = parsed.netloc.lower()
        return host[4:] if host.startswith("www.") else host
    except Exception:
        return ""


def source_paths() -> list[Path]:
    return sorted(SOURCES_DIR.glob("*/artworks.json"))


def merge_key(row: dict[str, Any]) -> str:
    url = normalize_url(str(row.get("url") or ""))
    title = normalize_title(str(row.get("title") or ""))
    artist = normalize_artist(str(row.get("artist") or ""))
    year = row.get("year")

    if url:
        return f"url:{url}"
    if title and artist and year:
        return f"tay:{title}|{artist}|{year}"
    if title and artist:
        return f"ta:{title}|{artist}"
    return f"t:{title}"


def preferred_title(records: list[dict[str, Any]]) -> str:
    scored: list[tuple[int, int, str]] = []
    for row in records:
        title = normalize_space(str(row.get("title") or ""))
        if not title:
            continue
        # Prefer non-URL-looking titles and longer descriptive strings.
        is_urlish = 1 if re.match(r"^https?://", title, re.I) else 0
        scored.append((is_urlish, -len(title), title))
    if not scored:
        return ""
    scored.sort()
    return scored[0][2]


def preferred_artist(records: list[dict[str, Any]]) -> str:
    for row in records:
        artist = normalize_space(str(row.get("artist") or ""))
        if artist:
            return artist
    return ""


def preferred_url(records: list[dict[str, Any]]) -> str:
    for row in records:
        url = normalize_url(str(row.get("url") or ""))
        if url:
            return url
    return ""


def collect_archive_urls(records: list[dict[str, Any]]) -> list[str]:
    urls = []
    for row in records:
        preservation = row.get("preservation") or {}
        archive_url = normalize_url(str(preservation.get("archive_url") or ""))
        if archive_url:
            urls.append(archive_url)
    return sorted(set(urls))


def collect_statuses(records: list[dict[str, Any]]) -> list[str]:
    statuses = []
    for row in records:
        preservation = row.get("preservation") or {}
        status = normalize_text(str(preservation.get("status") or ""))
        if status:
            statuses.append(status)
    return sorted(set(statuses))


def collect_technologies(records: list[dict[str, Any]]) -> list[str]:
    techs = []
    for row in records:
        for tech in row.get("technologies") or []:
            value = normalize_space(str(tech))
            if value:
                techs.append(value)
    return sorted(set(techs))


def inferred_evidence(records: list[dict[str, Any]], canonical_url: str) -> list[str]:
    evidence = set()
    host = url_host(canonical_url)
    if canonical_url.startswith("http://"):
        evidence.add("http-only-url")
    if host in {
        "geocities.com",
        "angelfire.com",
        "tripod.com",
        "yahoo.com",
        "myspace.com",
        "vine.co",
        "groups.yahoo.com",
        "answers.yahoo.com",
    }:
        evidence.add("historically-fragile-host")
    statuses = collect_statuses(records)
    if "dead" in statuses:
        evidence.add("source-marked-dead")
    if "degraded" in statuses:
        evidence.add("source-marked-degraded")
    if collect_archive_urls(records):
        evidence.add("archive-copy-known")
    techs = {t.lower() for t in collect_technologies(records)}
    extinct_stack = {
        "flash",
        "shockwave",
        "java",
        "java applet",
        "quicktime",
        "realplayer",
        "realaudio",
        "vrml",
        "silverlight",
        "director",
        "activex",
        "midi",
        "authorware",
        "smil",
        "beatnik",
        "pulse 3d",
    }
    if techs & extinct_stack:
        evidence.add("obsolete-runtime-tagged")
    return sorted(evidence)


def main() -> None:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    source_stats: dict[str, Any] = {}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for path in source_paths():
        rows = load_json(path)
        source_name = path.parent.name
        source_stats[source_name] = {"records": len(rows)}
        for row in rows:
            enriched = dict(row)
            enriched["_source_dir"] = source_name
            grouped[merge_key(enriched)].append(enriched)

    corpus = []
    queue = []

    for idx, (key, records) in enumerate(sorted(grouped.items()), start=1):
        title = preferred_title(records)
        artist = preferred_artist(records)
        canonical_url = preferred_url(records)
        years = [r.get("year") for r in records if isinstance(r.get("year"), int)]
        archive_urls = collect_archive_urls(records)
        statuses = collect_statuses(records)
        technologies = collect_technologies(records)
        evidence = inferred_evidence(records, canonical_url)
        source_names = sorted({r["_source_dir"] for r in records})

        corpus_id = f"na-{idx:06d}"
        corpus_row = {
            "corpus_id": corpus_id,
            "title": title,
            "artist": artist,
            "year": min(years) if years else None,
            "canonical_url": canonical_url,
            "canonical_host": url_host(canonical_url),
            "medium": "Net art",
            "technologies": technologies,
            "archive_urls": archive_urls,
            "source_names": source_names,
            "source_count": len(source_names),
            "merged_record_count": len(records),
            "source_statuses": statuses,
            "evidence_flags": evidence,
            "extinction_analysis": {
                "status": "unknown",
                "dependency_candidates": technologies,
                "extinction_event_candidates": [],
                "evidence_notes": [],
                "matched_event_ids": [],
            },
            "source_records": [
                {
                    "source": r.get("source", ""),
                    "source_dir": r["_source_dir"],
                    "source_id": r.get("source_id"),
                    "source_url": r.get("source_url", ""),
                    "title": r.get("title", ""),
                    "artist": r.get("artist", ""),
                    "year": r.get("year"),
                    "url": normalize_url(str(r.get("url") or "")),
                    "record_type": r.get("record_type"),
                    "tags": r.get("tags"),
                    "category": r.get("category"),
                    "series": r.get("series"),
                    "award": r.get("award"),
                    "section": r.get("section"),
                    "preservation": r.get("preservation", {}),
                }
                for r in records
            ],
        }
        corpus.append(corpus_row)

        queue.append(
            {
                "corpus_id": corpus_id,
                "title": title,
                "artist": artist,
                "canonical_url": canonical_url,
                "canonical_host": url_host(canonical_url),
                "technologies": technologies,
                "archive_urls": archive_urls,
                "evidence_flags": evidence,
                "source_statuses": statuses,
                "priority": (
                    100
                    + (20 if "obsolete-runtime-tagged" in evidence else 0)
                    + (15 if "source-marked-dead" in evidence else 0)
                    + (10 if "source-marked-degraded" in evidence else 0)
                    + (5 if archive_urls else 0)
                    + (3 if canonical_url.startswith("http://") else 0)
                ),
            }
        )

    queue.sort(key=lambda row: (-row["priority"], row["title"], row["artist"]))

    host_counter = Counter(row["canonical_host"] for row in corpus if row["canonical_host"])
    source_stats["_summary"] = {
        "merged_corpus_records": len(corpus),
        "high_priority_queue_records": len(queue),
        "top_hosts": host_counter.most_common(50),
    }

    (CORPUS_DIR / "netart-corpus.json").write_text(
        json.dumps(corpus, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CORPUS_DIR / "extinction-matching-queue.json").write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (CORPUS_DIR / "source-stats.json").write_text(
        json.dumps(source_stats, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
