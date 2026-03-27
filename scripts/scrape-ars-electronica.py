#!/usr/bin/env python3
"""
Scrape net art works from the Ars Electronica Prix archive.

The archive uses Django with DataTables. Approach:
1. Fetch /prix/data/?category=N to get year counts for net art (1995-2006)
2. For each year, fetch /prix/data/year/?year=YYYY&category=N to get work listings
3. Parse HTML fragments to extract work IDs, titles, artists, award levels
4. For each work, fetch /prix/{ID}/ to get full metadata
5. Save normalized JSON output
"""

import html
import json
import re
import sys
import time
from http.cookiejar import CookieJar
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPCookieProcessor

# ── Config ──────────────────────────────────────────────────────────────────

BASE_URL = "https://archive.aec.at"
CATEGORY = "N"
DELAY = 0.5  # seconds between requests

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "sources" / "ars-electronica" / "artworks.json"

# ── HTTP helpers ────────────────────────────────────────────────────────────

cookie_jar = CookieJar()
opener = build_opener(HTTPCookieProcessor(cookie_jar))

HEADERS = {
    "User-Agent": "NetArtExtinctionResearch/1.0 (academic research project)",
    "Accept": "application/json, text/html, */*",
    "X-Requested-With": "XMLHttpRequest",
}


def fetch(url, params=None):
    """Fetch a URL with GET, returning the response body as string."""
    if params:
        url = f"{url}?{urlencode(params)}"
    req = Request(url, headers=HEADERS)
    # Add CSRF token from cookies if available
    for cookie in cookie_jar:
        if cookie.name == "csrftoken":
            req.add_header("X-CSRFToken", cookie.value)
    resp = opener.open(req, timeout=30)
    return resp.read().decode("utf-8")


def fetch_json(url, params=None):
    """Fetch a URL and parse JSON response."""
    body = fetch(url, params)
    return json.loads(body)


# ── Parsing ─────────────────────────────────────────────────────────────────

def parse_year_html(html_str):
    """
    Parse the HTML fragment returned by /prix/data/year/ to extract works.

    Actual structure per work:
        <a class="boxlink prix" href="/prix/{ID}/" category="N">
          <div id="winner_{ID}" class="boxlink-inner">
            <div style="background-image:..." class="boxlink-inner-image"></div>
            <span class="award">Golden Nica</span>
            <div class="winner_title" id="winner_title_{ID}">Title</div>
          </div>
        </a>

    Award sections are separated by:
        <div class="winners_award">Golden Nica</div>

    Returns list of dicts with keys: source_id, title, award
    """
    works = []

    # Each <a class="boxlink prix"> is one work entry
    # We can extract: ID from href, title from winner_title div, award from span.award
    work_pattern = re.compile(
        r'<a[^>]*class="boxlink\s+prix"[^>]*href="/prix/(\d+)/"[^>]*>'
        r'(.*?)</a>',
        re.DOTALL,
    )

    for m in work_pattern.finditer(html_str):
        work_id = m.group(1)
        inner = m.group(2)

        # Title from <div class="winner_title" ...>Title</div>
        title_m = re.search(
            r'<div[^>]*class="winner_title"[^>]*>(.*?)</div>',
            inner, re.DOTALL,
        )
        title = html.unescape(strip_tags(title_m.group(1)).strip()) if title_m else ""

        # Award from <span class="award">Award Name</span>
        award_m = re.search(
            r'<span[^>]*class="award"[^>]*>(.*?)</span>',
            inner, re.DOTALL,
        )
        award_raw = strip_tags(award_m.group(1)).strip() if award_m else ""

        # Normalize award names
        if "golden" in award_raw.lower() or "nica" in award_raw.lower():
            award = "Golden Nica"
        elif "distinction" in award_raw.lower():
            award = "Award of Distinction"
        elif "honorary" in award_raw.lower() or "mention" in award_raw.lower():
            award = "Honorary Mention"
        else:
            award = award_raw or "Unknown"

        works.append({
            "source_id": work_id,
            "title": title,
            "artist": "",  # not available in listing, fetched from detail
            "award": award,
        })

    return works


def strip_tags(text):
    """Remove HTML tags from a string."""
    return re.sub(r'<[^>]+>', '', text)


def parse_detail_page(html_str, work_id):
    """
    Parse a work detail page at /prix/{ID}/ to extract full metadata.

    Actual page structure:
        <h3 class="bar-color">
          Category Name  <span>Award Name YYYY</span>
        </h3>
        <h1 style="...">Title</h1>
        <div class="mb-1">Artist Name</div>
        <div id="tab-1" class="tab-pane ...">Description text...
            Links: <a href="http://...">http://...</a>
        </div>

    Returns dict with: title, artist, year, category, award, description, url
    """
    info = {}

    # Title from <h1 style="...font-size: 20px...">Title</h1>
    # The page has multiple h1 tags; the work title is the one with inline font-size
    title_m = re.search(
        r'<h1[^>]*style="[^"]*font-size:\s*20px[^"]*"[^>]*>(.*?)</h1>',
        html_str, re.DOTALL,
    )
    if not title_m:
        # Fallback: last h1 on the page (skip nav/header ones)
        all_h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', html_str, re.DOTALL)
        if all_h1:
            title_m_text = all_h1[-1]
            info["title"] = html.unescape(strip_tags(title_m_text)).strip()
    if title_m:
        info["title"] = html.unescape(strip_tags(title_m.group(1))).strip()

    # Category and Award from <h3 class="bar-color">
    # Format: "Category Name  <span ...>Award - Award Name YYYY</span>"
    h3_m = re.search(
        r'<h3[^>]*class="bar-color"[^>]*>(.*?)</h3>',
        html_str, re.DOTALL,
    )
    if h3_m:
        h3_content = h3_m.group(1)
        # Extract the span (award + year)
        span_m = re.search(r'<span[^>]*>(.*?)</span>', h3_content, re.DOTALL)
        if span_m:
            award_text = strip_tags(span_m.group(1)).strip()
            # Parse "Goldene Nica - Golden Nica 2001" or "Award of Distinction 2001"
            # Normalize award
            if "golden" in award_text.lower() or "nica" in award_text.lower():
                info["award"] = "Golden Nica"
            elif "distinction" in award_text.lower():
                info["award"] = "Award of Distinction"
            elif "honorary" in award_text.lower() or "mention" in award_text.lower():
                info["award"] = "Honorary Mention"
            else:
                # Strip year from end
                info["award"] = re.sub(r'\s*\d{4}\s*$', '', award_text).strip()

            # Extract year from award text
            year_m = re.search(r'(\d{4})', award_text)
            if year_m:
                info["year"] = int(year_m.group(1))

        # Category is the text before the span
        cat_text = re.sub(r'<span.*?</span>', '', h3_content, flags=re.DOTALL)
        cat_text = strip_tags(cat_text).strip()
        if cat_text:
            info["category"] = cat_text

    # Artist: appears in <div class="mb-1"> right after <h1>
    # Structure: <h1>Title</h1> ... <div class="mb-1"> artist names </div>
    artist_m = re.search(
        r'font-size:\s*20px[^>]*>.*?</h1>.*?'
        r'<div[^>]*class="mb-1"[^>]*>(.*?)</div>',
        html_str, re.DOTALL,
    )
    if artist_m:
        artist_raw = artist_m.group(1)
        # May contain <a> tags or plain text with newlines
        artist_links = re.findall(r'<a[^>]*>(.*?)</a>', artist_raw)
        if artist_links:
            names = [strip_tags(a).strip() for a in artist_links if strip_tags(a).strip()]
            info["artist"] = html.unescape(", ".join(names))
        else:
            # Clean up whitespace from inline formatting
            text = strip_tags(artist_raw)
            # Collapse whitespace and clean comma separation
            text = re.sub(r'\s+', ' ', text).strip()
            # Remove trailing commas
            text = re.sub(r',\s*$', '', text).strip()
            info["artist"] = html.unescape(text)

    # Description from tab-1 (the jury statement / main description)
    # tab-1 content extends until the next tab-pane or closing structure
    desc_m = re.search(
        r'<div[^>]*id="tab-1"[^>]*class="tab-pane[^"]*"[^>]*>(.*?)'
        r'(?:</div>\s*<div[^>]*id="tab-|</div>\s*</div>\s*</div>)',
        html_str, re.DOTALL,
    )
    if not desc_m:
        # Simpler fallback
        desc_m = re.search(
            r'<div[^>]*id="tab-1"[^>]*>(.*?)(?:\n\s*</div>)',
            html_str, re.DOTALL,
        )
    if desc_m:
        desc_raw = desc_m.group(1)
        # Remove "Links:" section from description
        desc_clean = re.split(r'<br\s*/?>\s*<br\s*/?>\s*Links:', desc_raw, flags=re.IGNORECASE)[0]
        text = html.unescape(strip_tags(desc_clean)).strip()
        # Collapse excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        info["description"] = text

    # Project URL from "Links: <a href="...">" in tab content
    link_m = re.search(
        r'Links:\s*<a[^>]*href="(https?://[^"]+)"',
        html_str, re.IGNORECASE,
    )
    if link_m:
        info["url"] = link_m.group(1)
    else:
        # Fallback: look for rel="nofollow" links (external project links)
        nofollow_links = re.findall(
            r'<a[^>]*rel="nofollow"[^>]*href="(https?://[^"]+)"', html_str
        )
        if not nofollow_links:
            nofollow_links = re.findall(
                r'<a[^>]*href="(https?://[^"]+)"[^>]*rel="nofollow"', html_str
            )
        # Filter out ars electronica's own URLs
        external = [
            u for u in nofollow_links
            if "aec.at" not in u and "electronica" not in u
        ]
        if external:
            info["url"] = external[0]

    return info


# ── Main scrape logic ───────────────────────────────────────────────────────

def main():
    print("=== Ars Electronica Prix Net Art Scraper ===\n")

    # Step 1: Initialize session by fetching main page (get cookies/CSRF)
    print("Fetching main archive page for session...")
    fetch(f"{BASE_URL}/prix/")
    time.sleep(DELAY)

    # Step 2: Fetch category data to get year counts
    print(f"Fetching category '{CATEGORY}' data...")
    data = fetch_json(f"{BASE_URL}/prix/data/", {"category": CATEGORY})
    time.sleep(DELAY)

    year_counts = data.get("aaYearCounts", [])
    total_display = data.get("iTotalDisplayRecords", 0)
    print(f"Found {total_display} works across {len(year_counts)} years")

    for yc in year_counts:
        print(f"  {yc[0]}: {yc[1]} works")

    # Step 3: For each year, fetch the winners list
    all_works = []
    seen_ids = set()

    for year_str, count in year_counts:
        year = int(year_str)
        print(f"\nFetching {year} ({count} works)...")

        year_html = fetch(f"{BASE_URL}/prix/data/year/", {
            "year": year,
            "category": CATEGORY,
        })
        time.sleep(DELAY)

        works = parse_year_html(year_html)
        print(f"  Parsed {len(works)} works from HTML")

        for w in works:
            if w["source_id"] in seen_ids:
                continue
            seen_ids.add(w["source_id"])
            w["year"] = year
            all_works.append(w)

        if len(works) != count:
            print(f"  WARNING: Expected {count}, got {len(works)}")

    print(f"\nTotal works from listings: {len(all_works)}")

    # Step 4: Fetch detail pages for each work
    artworks = []
    for i, work in enumerate(all_works):
        wid = work["source_id"]
        print(f"  [{i+1}/{len(all_works)}] Fetching detail for {wid}: {work['title'][:40]}...")

        try:
            detail_html = fetch(f"{BASE_URL}/prix/{wid}/")
            detail = parse_detail_page(detail_html, wid)
        except Exception as e:
            print(f"    ERROR fetching detail: {e}")
            detail = {}

        time.sleep(DELAY)

        # Build normalized record, preferring detail page data
        record = {
            "source": "ars-electronica",
            "source_id": wid,
            "source_url": f"https://archive.aec.at/prix/{wid}/",
            "title": detail.get("title", work["title"]),
            "artist": detail.get("artist", work["artist"]),
            "year": detail.get("year", work["year"]),
            "url": detail.get("url", ""),
            "medium": "Net art",
            "award": detail.get("award", work["award"]),
            "category": detail.get("category", "Net-based Art"),
            "description": detail.get("description", ""),
            "technologies": [],
            "preservation": {"status": "unknown"},
        }
        artworks.append(record)

    # Step 5: Save output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(artworks)} artworks to {OUTPUT_FILE}")

    # Summary stats
    awards = {}
    for a in artworks:
        awards[a["award"]] = awards.get(a["award"], 0) + 1
    print("\nAward breakdown:")
    for award, count in sorted(awards.items()):
        print(f"  {award}: {count}")

    years = {}
    for a in artworks:
        years[a["year"]] = years.get(a["year"], 0) + 1
    print("\nYear breakdown:")
    for year, count in sorted(years.items()):
        print(f"  {year}: {count}")

    with_url = sum(1 for a in artworks if a["url"])
    with_desc = sum(1 for a in artworks if a["description"])
    print(f"\nWith project URL: {with_url}/{len(artworks)}")
    print(f"With description: {with_desc}/{len(artworks)}")


if __name__ == "__main__":
    main()
