#!/usr/bin/env python3
"""Scrape artworks from the LIMA (li-ma.nl) catalogue via their Strapi API.

LIMA (Living Media Art) is a Dutch media art preservation organisation based
in Amsterdam.  Their Gatsby front-end loads artwork data from a public Strapi
API whose bearer token is embedded in the compiled JS bundle.  We paginate
through the API (100 items/page, ~31 pages for ~3 000 works) with a polite
1-second delay between requests.

Only stdlib is used: urllib, json, time, pathlib.
"""

import json
import time
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_API = "https://li-ma.nl/strapi/api/artworks"
# Public read-only token shipped in the front-end JS bundle
TOKEN = (
    "b4b8887fa89f1d3cc7c1190aacf91508c76bd12e1a42d665146700590efe04c3"
    "5ec10b8d917ac0888bb0ce59dc45621494fe45777cce8afc993efb503276ad18"
    "acd946dcfa1c1cedeb14e3d8824815a6128496bd063776a83884522fa6eb2bae"
    "72ebf2057bcc55ad7c2b1f2fe9b0c9aa96cd6574c8a788a5e3dce17893df0620"
)
PAGE_SIZE = 100
DELAY = 1.0  # seconds between requests
UA = "Mozilla/5.0 (compatible; netart-extinction research bot)"
SOURCE_URL = "https://www.li-ma.nl/lima/catalogue"
OUT_PATH = Path(__file__).resolve().parent / "artworks.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fetch_page(page: int) -> dict:
    """Fetch one page of artworks from the Strapi API."""
    url = (
        f"{BASE_API}"
        f"?sort=titleOrder:asc"
        f"&pagination[page]={page}"
        f"&pagination[pageSize]={PAGE_SIZE}"
    )
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Authorization": f"Bearer {TOKEN}",
    })
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode("utf-8"))


def normalise(item: dict) -> dict:
    """Convert a Strapi artwork record to our standard format."""
    attrs = item.get("attributes", {})

    # Build the canonical URL for this artwork
    artwork_url = attrs.get("artworkUrl") or ""
    if not artwork_url:
        # Fallback: construct from the LIMA catalogue path
        artwork_url = f"https://www.li-ma.nl/lima/catalogue/art/{item['id']}"

    # Determine medium from the type field (video, installation, etc.)
    raw_type = (attrs.get("type") or "").strip()
    medium = raw_type.capitalize() if raw_type else "Media art"

    # Year may be null/0 in some records
    year = attrs.get("year")
    if not year or year == 0:
        year = None

    return {
        "source": "lima",
        "source_url": SOURCE_URL,
        "title": (attrs.get("title") or "").strip(),
        "artist": (attrs.get("artistName") or "").strip(),
        "year": year,
        "url": artwork_url,
        "medium": medium,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"Scraping LIMA catalogue from {BASE_API}")

    artworks = []
    page = 1
    total_pages = None

    while True:
        print(f"  Fetching page {page}" + (f"/{total_pages}" if total_pages else "") + " ...")
        try:
            data = fetch_page(page)
        except Exception as e:
            print(f"  ERROR on page {page}: {e}")
            break

        pagination = data.get("meta", {}).get("pagination", {})
        total_pages = pagination.get("pageCount", 0)
        total_items = pagination.get("total", 0)

        items = data.get("data", [])
        if not items:
            break

        for item in items:
            rec = normalise(item)
            if rec["title"]:  # skip empty records
                artworks.append(rec)

        if page >= total_pages:
            break

        page += 1
        time.sleep(DELAY)

    # Deduplicate by URL
    seen = set()
    unique = []
    for a in artworks:
        if a["url"] not in seen:
            seen.add(a["url"])
            unique.append(a)
    artworks = unique

    print(f"\nCollected {len(artworks)} artworks (from {total_items} total API records)")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
