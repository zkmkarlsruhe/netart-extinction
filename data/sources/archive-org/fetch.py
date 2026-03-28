#!/usr/bin/env python3
"""Fetch net art collections from Internet Archive Search API."""

import json
import re
import sys
import time
import urllib.request
import urllib.parse
from collections import OrderedDict

QUERIES = [
    'subject:"net art"',
    'subject:"internet art"',
    'subject:"web art"',
    'collection:"rhizome"',
    'collection:"archiveteam-geocities"',
]

FIELDS = ["identifier", "title", "creator", "date", "description"]
ROWS = 500
BASE = "https://archive.org/advancedsearch.php"


def build_url(query):
    params = [("q", query), ("output", "json"), ("rows", str(ROWS))]
    for f in FIELDS:
        params.append(("fl[]", f))
    return BASE + "?" + urllib.parse.urlencode(params)


def fetch_query(query):
    url = build_url(query)
    print(f"  Fetching: {query}", file=sys.stderr)
    print(f"  URL: {url}", file=sys.stderr)
    req = urllib.request.Request(url, headers={"User-Agent": "netart-research/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        docs = data.get("response", {}).get("docs", [])
        print(f"  Got {len(docs)} results", file=sys.stderr)
        return docs
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return []


def extract_year(date_str):
    """Extract a 4-digit year from a date string."""
    if not date_str:
        return None
    m = re.search(r"(19|20)\d{2}", str(date_str))
    return int(m.group(0)) if m else None


def normalize(doc):
    identifier = doc.get("identifier", "")
    title = doc.get("title", "")
    creator = doc.get("creator", "")
    date = doc.get("date", "")
    description = doc.get("description", "")

    # Handle lists (IA sometimes returns arrays)
    if isinstance(title, list):
        title = title[0] if title else ""
    if isinstance(creator, list):
        creator = "; ".join(creator)
    if isinstance(description, list):
        description = " ".join(description)
    if isinstance(date, list):
        date = date[0] if date else ""

    # Truncate very long descriptions
    if len(str(description)) > 500:
        description = str(description)[:497] + "..."

    year = extract_year(date)

    return OrderedDict([
        ("source", "archive-org"),
        ("source_id", identifier),
        ("source_url", f"https://archive.org/details/{identifier}"),
        ("title", str(title).strip()),
        ("artist", str(creator).strip()),
        ("year", year),
        ("medium", "Net art"),
        ("description", str(description).strip()),
    ])


def main():
    seen = set()
    artworks = []

    for query in QUERIES:
        docs = fetch_query(query)
        for doc in docs:
            ident = doc.get("identifier", "")
            if ident and ident not in seen:
                seen.add(ident)
                artworks.append(normalize(doc))
        time.sleep(1)  # be polite

    # Sort by year (None last), then title
    artworks.sort(key=lambda x: (x["year"] is None, x["year"] or 9999, x["title"]))

    out_path = "/x/coding/03-websites/netart-extinction/data/sources/archive-org/artworks.json"
    with open(out_path, "w") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(artworks)} unique artworks to {out_path}", file=sys.stderr)

    # Print some stats
    with_year = sum(1 for a in artworks if a["year"])
    with_artist = sum(1 for a in artworks if a["artist"])
    print(f"  With year: {with_year}", file=sys.stderr)
    print(f"  With artist: {with_artist}", file=sys.stderr)
    years = [a["year"] for a in artworks if a["year"]]
    if years:
        print(f"  Year range: {min(years)}-{max(years)}", file=sys.stderr)


if __name__ == "__main__":
    main()
