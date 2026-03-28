#!/usr/bin/env python3
"""
Scrape software art projects from Runme.org.

Strategy:
1. Discover all project slugs via the Wayback Machine CDX API
   (gives ~486 unique slugs across the full archive history).
2. Fetch each project page from the LIVE site (runme.org is still up
   in archive mode) with a 2-second delay between requests.
3. Parse title, artist, year, URL, keywords, and category from the
   project page HTML using only Python stdlib (re + html.parser).
4. Output to artworks.json.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from html import unescape

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "artworks.json")
SLUGS_CACHE = os.path.join(OUTPUT_DIR, "slugs_cache.json")

BASE_URL = "https://runme.org"
CDX_API = (
    "http://web.archive.org/cdx/search/cdx"
    "?url=runme.org/project/*"
    "&output=json&fl=original&collapse=urlkey&limit=2000"
)

HEADERS = {
    "User-Agent": "NetArtExtinctionResearch/1.0 (academic research; polite scraper)"
}


def fetch(url, retries=3, delay=2):
    """Fetch a URL, return decoded text or None."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                # Try to detect encoding
                ct = resp.headers.get("Content-Type", "")
                if "charset=" in ct:
                    enc = ct.split("charset=")[-1].strip()
                else:
                    enc = "utf-8"
                try:
                    return data.decode(enc)
                except (UnicodeDecodeError, LookupError):
                    return data.decode("latin-1")
        except Exception as e:
            print(f"  [!] Attempt {attempt+1} failed for {url}: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(delay)
    return None


def discover_slugs():
    """Get all project slugs from CDX API, with caching."""
    if os.path.exists(SLUGS_CACHE):
        print(f"Loading cached slugs from {SLUGS_CACHE}")
        with open(SLUGS_CACHE, "r") as f:
            return json.load(f)

    print("Fetching project slugs from Wayback CDX API...")
    text = fetch(CDX_API)
    if not text:
        print("ERROR: Could not fetch CDX data", file=sys.stderr)
        return []

    data = json.loads(text)
    slugs = set()
    for row in data[1:]:  # skip header row
        url = urllib.parse.unquote(row[0])
        # Match /project/+SLUG/ or /project/ SLUG/ (root project pages)
        m = re.match(
            r"https?://(?:www\.)?runme\.org(?::80)?/project/\s*\+?([A-Za-z0-9_\-\.]+)/?$",
            url,
        )
        if m:
            slugs.add(m.group(1))

    slugs = sorted(slugs)
    print(f"Found {len(slugs)} unique project slugs from CDX")

    # Save cache
    with open(SLUGS_CACHE, "w") as f:
        json.dump(slugs, f, indent=2)

    return slugs


def extract_year_from_keywords(keywords):
    """Look for a 4-digit year in the keyword list."""
    for kw in keywords:
        m = re.match(r"^(19\d{2}|20[0-2]\d)$", kw.strip())
        if m:
            return int(m.group(1))
    return None


def extract_year_from_date(date_str):
    """Extract year from upload date like '30 Jan 2003'."""
    m = re.search(r"(19\d{2}|20[0-2]\d)", date_str)
    if m:
        return int(m.group(1))
    return None


def parse_project_page(html, slug):
    """Parse a project page and return a dict, or None if invalid."""
    # Title: <font class="title">TITLE</font>
    title_m = re.search(r'<font\s+class="title">(.*?)</font>', html, re.DOTALL)
    if not title_m:
        return None
    title = unescape(title_m.group(1)).strip()

    # Artist: comes after </font><br />ARTIST</b>
    # Pattern: class="title">TITLE</font><br />ARTIST</b>
    artist_m = re.search(
        r'class="title">.*?</font>\s*<br\s*/?>\s*(.*?)\s*</b>',
        html,
        re.DOTALL,
    )
    artist = ""
    if artist_m:
        artist = unescape(artist_m.group(1)).strip()
        # Clean up HTML tags within artist name
        artist = re.sub(r"<[^>]+>", "", artist).strip()

    # Project homepage URL
    homepage_m = re.search(
        r'project homepage:\s*<a\s+href="([^"]+)"', html
    )
    homepage = homepage_m.group(1) if homepage_m else None

    # Download URL (artwork file)
    download_m = re.search(
        r'download\s*<a\s+href="([^"]+)"', html
    )
    download_url = download_m.group(1) if download_m else None

    # Artwork URL: prefer homepage, fallback to download
    artwork_url = homepage or download_url or ""

    # Keywords: extract from keyword links
    keywords = re.findall(
        r'href="../../keywords/\+([^"]+)/index\.html"', html
    )
    keywords = [urllib.parse.unquote(k).replace("_", " ") for k in keywords]

    # Category
    cat_m = re.findall(
        r'href="../../categories/\+([^"]+)/index\.html"', html
    )
    categories = [
        unescape(urllib.parse.unquote(c)).replace("_", " ").replace("+", " ").strip()
        for c in cat_m
    ]
    category = " / ".join(categories) if categories else "Software art"

    # Upload date
    date_m = re.search(
        r"uploaded by.*?,\s*(\d{1,2}\s+\w+\s+\d{4})", html
    )
    upload_date = date_m.group(1) if date_m else None

    # Year: prefer keyword year, then upload date year
    year = extract_year_from_keywords(keywords)
    if year is None and upload_date:
        year = extract_year_from_date(upload_date)

    # Source URL for this project on runme.org
    source_url = f"{BASE_URL}/project/+{slug}/"

    return {
        "source": "runme",
        "source_url": source_url,
        "title": title,
        "artist": artist or None,
        "year": year,
        "url": artwork_url or None,
        "medium": "Software art",
        "category": category,
        "keywords": [k for k in keywords if not re.match(r"^(19|20)\d{2}$", k)],
    }


def main():
    slugs = discover_slugs()
    if not slugs:
        print("No slugs found. Exiting.", file=sys.stderr)
        sys.exit(1)

    # Load existing results for resume capability
    artworks = []
    seen_slugs = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            artworks = json.load(f)
        for a in artworks:
            # Extract slug from source_url
            m = re.search(r"/project/\+([^/]+)/", a.get("source_url", ""))
            if m:
                seen_slugs.add(m.group(1))
        print(f"Resuming: {len(seen_slugs)} projects already scraped")

    total = len(slugs)
    errors = 0
    skipped = 0

    for i, slug in enumerate(slugs, 1):
        if slug in seen_slugs:
            continue

        url = f"{BASE_URL}/project/+{slug}/"
        print(f"[{i}/{total}] Fetching {slug}...", end=" ", flush=True)

        html = fetch(url, retries=2, delay=2)
        if not html:
            print("FAILED")
            errors += 1
            # Still delay between requests
            time.sleep(2)
            continue

        artwork = parse_project_page(html, slug)
        if artwork:
            artworks.append(artwork)
            print(f"OK - {artwork['title']} by {artwork['artist']}")
        else:
            print("SKIP (could not parse)")
            skipped += 1

        # Save incrementally every 50 projects
        if len(artworks) % 50 == 0:
            with open(OUTPUT_FILE, "w") as f:
                json.dump(artworks, f, indent=2, ensure_ascii=False)

        # Polite delay between requests
        time.sleep(2)

    # Final save
    # Sort by title
    artworks.sort(key=lambda a: (a.get("title") or "").lower())

    with open(OUTPUT_FILE, "w") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Scraped {len(artworks)} artworks ({errors} errors, {skipped} skipped)")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
