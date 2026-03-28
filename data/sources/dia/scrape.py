#!/usr/bin/env python3
"""
Scrape Dia Art Foundation's Artist Web Projects listing.
https://www.diaart.org/program/artistswebprojects

The listing paginates via /page/N URLs that accumulate all items.
Page 0 (base) shows ~20 items; /page/2 shows all ~40.
We fetch pages until no new items appear.

Output: data/sources/dia/artworks.json
"""

import json
import re
import time
import urllib.request
import html as html_module
from pathlib import Path

BASE_URL = "https://www.diaart.org/program/artistswebprojects"
SOURCE_URL = BASE_URL
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = SCRIPT_DIR / "artworks.json"


def fetch(url):
    """Fetch a URL and return its text content."""
    print(f"  Fetching {url}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def strip_tags(s):
    """Remove HTML tags and decode entities."""
    s = html_module.unescape(s)
    s = re.sub(r"<[^>]+>", "", s)
    return s.strip()


def parse_artist_title(raw_title):
    """
    Split 'Artist, Title' or 'Artist: Title' from the item-title text.
    Some entries have no comma/colon separator (e.g. the first entry).

    The raw HTML typically has:
      Artist, <em>Title</em>
      Artist: <em>Title</em>
    or just a plain title with no artist prefix.
    """
    # First, try to extract title from <em> or <i> tags before stripping
    em_match = re.search(r"<(?:em|i)>(.*?)</(?:em|i)>", raw_title)
    title_from_em = strip_tags(em_match.group(1)).strip() if em_match else None

    plain = strip_tags(raw_title)

    if title_from_em:
        # Everything before the <em>/<i> tag is artist (strip trailing comma/colon/space)
        before_em = re.split(r"<(?:em|i)>", raw_title)[0]
        artist = strip_tags(before_em).rstrip(",: \xa0").strip()
        return artist, title_from_em

    # No <em>/<i> — try splitting on comma or colon
    for sep in [": ", ", "]:
        if sep in plain:
            parts = plain.split(sep, 1)
            return parts[0].strip(), parts[1].strip()

    # No clear separator — title only (artist unknown)
    return None, plain


def parse_year_from_date(date_str):
    """Extract year from strings like 'Launch date: March 30, 2004' or 'Part II Launched March 5, 2022'."""
    m = re.search(r"(\d{4})", date_str)
    return int(m.group(1)) if m else None


def parse_items(html_text):
    """Parse grid items from the Artist Web Projects listing page."""
    # Pattern for each grid item: captures title HTML, date/description, and link href
    pattern = re.compile(
        r'<div class="grid-item small">\s*<figure class="item">.*?'
        r'<h2 class="item-title">(.*?)</h2>'
        r".*?<p>(.*?)</figcaption"
        r'.*?<a href="([^"]+)"',
        re.DOTALL,
    )

    artworks = []
    seen_hrefs = set()

    for m in pattern.finditer(html_text):
        title_html = m.group(1)
        date_html = m.group(2)
        href = m.group(3)

        # Strip /page/N suffix from href (artifact of pagination URL)
        href_clean = re.sub(r"/page/\d+$", "", href)

        # Deduplicate (pagination accumulates)
        if href_clean in seen_hrefs:
            continue
        seen_hrefs.add(href_clean)

        artist, title = parse_artist_title(title_html)
        date_text = strip_tags(date_html)
        year = parse_year_from_date(date_text)

        # Ensure full URL
        if href_clean.startswith("/"):
            url = "https://www.diaart.org" + href_clean
        else:
            url = href_clean

        entry = {
            "source": "dia",
            "source_url": SOURCE_URL,
            "title": title,
            "artist": artist,
            "year": year,
            "url": url,
            "medium": "Net art",
        }
        artworks.append(entry)

    return artworks


def main():
    print("Scraping Dia Art Foundation - Artist Web Projects")
    print(f"Source: {SOURCE_URL}")

    # The site uses cumulative pagination: /page/N returns all items
    # from pages 0..N.  Page 0 and /page/1 both show the first 20;
    # /page/2 shows 40, etc.  We step by 2 to actually advance.
    best_html = ""
    best_count = 0

    for page_num in [0, 2, 4, 6, 8, 10]:
        if page_num == 0:
            url = BASE_URL
        else:
            url = f"{BASE_URL}/page/{page_num}"

        try:
            html_text = fetch(url)
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            break

        items = parse_items(html_text)
        count = len(items)
        print(f"  Page {page_num}: {count} unique items found")

        if count > best_count:
            best_html = html_text
            best_count = count
        else:
            print("  No new items, stopping pagination.")
            break

        time.sleep(1)

    # Final parse from the page with most items
    artworks = parse_items(best_html)
    print(f"\nTotal artworks found: {len(artworks)}")

    # Fix known entries where the listing page omits the artist name
    ARTIST_FIXES = {
        "May amnesia never kiss us on the mouth": "Basel Abbas and Ruanne Abou-Rahme",
    }
    for a in artworks:
        if a["artist"] is None and a["title"] in ARTIST_FIXES:
            a["artist"] = ARTIST_FIXES[a["title"]]

    # Sort by year (oldest first), then title
    artworks.sort(key=lambda a: (a["year"] or 9999, a["title"]))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"Saved to {OUTPUT_PATH}")
    print()
    for a in artworks:
        print(f"  {a['year']}  {a['artist'] or '?':40s}  {a['title']}")


if __name__ == "__main__":
    main()
