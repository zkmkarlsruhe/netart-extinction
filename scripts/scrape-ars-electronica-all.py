#!/usr/bin/env python3
"""
Scrape art-relevant works from the Ars Electronica Prix archive.

Categories scraped:
  N   - Net Art (net-based art, 1995-2006)
  IA  - Interactive Art
  HA  - Hybrid Art
  DC  - Digital Communities
  AIA - AI in Art Award

Approach per category:
1. GET /prix/data/?category=XX  -> year counts
2. GET /prix/data/year/?year=YYYY&category=XX  -> work IDs per year
3. GET /prix/{ID}/  -> full metadata per work

Skips IDs already present in the existing artworks.json to avoid re-fetching.
Saves all results (including existing net art) to artworks-all.json.
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

# -- Config ------------------------------------------------------------------

BASE_URL = "https://archive.aec.at"
DELAY = 0.5  # seconds between requests

CATEGORIES = [
    ("N",   "Net Art"),
    ("IA",  "Interactive Art"),
    ("HA",  "Hybrid Art"),
    ("DC",  "Digital Communities"),
    ("AIA", "AI in Art Award"),
]

# Default medium label per category code
MEDIUM_MAP = {
    "N":   "Net art",
    "IA":  "Interactive art",
    "HA":  "Hybrid art",
    "DC":  "Digital communities",
    "AIA": "AI art",
}

PROJECT_ROOT = Path(__file__).parent.parent
EXISTING_FILE = PROJECT_ROOT / "data" / "sources" / "ars-electronica" / "artworks.json"
OUTPUT_FILE = PROJECT_ROOT / "data" / "sources" / "ars-electronica" / "artworks-all.json"

# -- HTTP helpers ------------------------------------------------------------

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
    for cookie in cookie_jar:
        if cookie.name == "csrftoken":
            req.add_header("X-CSRFToken", cookie.value)
    resp = opener.open(req, timeout=30)
    return resp.read().decode("utf-8")


def fetch_json(url, params=None):
    """Fetch a URL and parse JSON response."""
    body = fetch(url, params)
    return json.loads(body)


# -- Parsing -----------------------------------------------------------------

def strip_tags(text):
    """Remove HTML tags from a string."""
    return re.sub(r'<[^>]+>', '', text)


def parse_year_html(html_str):
    """
    Parse the HTML fragment returned by /prix/data/year/ to extract works.
    Returns list of dicts with keys: source_id, title, award
    """
    works = []
    work_pattern = re.compile(
        r'<a[^>]*class="boxlink\s+prix"[^>]*href="/prix/(\d+)/"[^>]*>'
        r'(.*?)</a>',
        re.DOTALL,
    )

    for m in work_pattern.finditer(html_str):
        work_id = m.group(1)
        inner = m.group(2)

        title_m = re.search(
            r'<div[^>]*class="winner_title"[^>]*>(.*?)</div>',
            inner, re.DOTALL,
        )
        title = html.unescape(strip_tags(title_m.group(1)).strip()) if title_m else ""

        award_m = re.search(
            r'<span[^>]*class="award"[^>]*>(.*?)</span>',
            inner, re.DOTALL,
        )
        award_raw = strip_tags(award_m.group(1)).strip() if award_m else ""

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
            "artist": "",
            "award": award,
        })

    return works


def parse_detail_page(html_str, work_id):
    """
    Parse a work detail page at /prix/{ID}/ to extract full metadata.
    Returns dict with: title, artist, year, category, award, description, url
    """
    info = {}

    # Title
    title_m = re.search(
        r'<h1[^>]*style="[^"]*font-size:\s*20px[^"]*"[^>]*>(.*?)</h1>',
        html_str, re.DOTALL,
    )
    if not title_m:
        all_h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', html_str, re.DOTALL)
        if all_h1:
            info["title"] = html.unescape(strip_tags(all_h1[-1])).strip()
    if title_m:
        info["title"] = html.unescape(strip_tags(title_m.group(1))).strip()

    # Category and Award from <h3 class="bar-color">
    h3_m = re.search(
        r'<h3[^>]*class="bar-color"[^>]*>(.*?)</h3>',
        html_str, re.DOTALL,
    )
    if h3_m:
        h3_content = h3_m.group(1)
        span_m = re.search(r'<span[^>]*>(.*?)</span>', h3_content, re.DOTALL)
        if span_m:
            award_text = strip_tags(span_m.group(1)).strip()
            if "golden" in award_text.lower() or "nica" in award_text.lower():
                info["award"] = "Golden Nica"
            elif "distinction" in award_text.lower():
                info["award"] = "Award of Distinction"
            elif "honorary" in award_text.lower() or "mention" in award_text.lower():
                info["award"] = "Honorary Mention"
            else:
                info["award"] = re.sub(r'\s*\d{4}\s*$', '', award_text).strip()

            year_m = re.search(r'(\d{4})', award_text)
            if year_m:
                info["year"] = int(year_m.group(1))

        cat_text = re.sub(r'<span.*?</span>', '', h3_content, flags=re.DOTALL)
        cat_text = strip_tags(cat_text).strip()
        if cat_text:
            info["category"] = cat_text

    # Artist
    artist_m = re.search(
        r'font-size:\s*20px[^>]*>.*?</h1>.*?'
        r'<div[^>]*class="mb-1"[^>]*>(.*?)</div>',
        html_str, re.DOTALL,
    )
    if artist_m:
        artist_raw = artist_m.group(1)
        artist_links = re.findall(r'<a[^>]*>(.*?)</a>', artist_raw)
        if artist_links:
            names = [strip_tags(a).strip() for a in artist_links if strip_tags(a).strip()]
            info["artist"] = html.unescape(", ".join(names))
        else:
            text = strip_tags(artist_raw)
            text = re.sub(r'\s+', ' ', text).strip()
            text = re.sub(r',\s*$', '', text).strip()
            info["artist"] = html.unescape(text)

    # Description from tab-1
    desc_m = re.search(
        r'<div[^>]*id="tab-1"[^>]*class="tab-pane[^"]*"[^>]*>(.*?)'
        r'(?:</div>\s*<div[^>]*id="tab-|</div>\s*</div>\s*</div>)',
        html_str, re.DOTALL,
    )
    if not desc_m:
        desc_m = re.search(
            r'<div[^>]*id="tab-1"[^>]*>(.*?)(?:\n\s*</div>)',
            html_str, re.DOTALL,
        )
    if desc_m:
        desc_raw = desc_m.group(1)
        desc_clean = re.split(r'<br\s*/?>\s*<br\s*/?>\s*Links:', desc_raw, flags=re.IGNORECASE)[0]
        text = html.unescape(strip_tags(desc_clean)).strip()
        text = re.sub(r'\s+', ' ', text)
        info["description"] = text

    # Project URL
    link_m = re.search(
        r'Links:\s*<a[^>]*href="(https?://[^"]+)"',
        html_str, re.IGNORECASE,
    )
    if link_m:
        info["url"] = link_m.group(1)
    else:
        nofollow_links = re.findall(
            r'<a[^>]*rel="nofollow"[^>]*href="(https?://[^"]+)"', html_str
        )
        if not nofollow_links:
            nofollow_links = re.findall(
                r'<a[^>]*href="(https?://[^"]+)"[^>]*rel="nofollow"', html_str
            )
        external = [
            u for u in nofollow_links
            if "aec.at" not in u and "electronica" not in u
        ]
        if external:
            info["url"] = external[0]

    return info


# -- Main scrape logic -------------------------------------------------------

def main():
    print("=== Ars Electronica Prix Multi-Category Scraper ===\n")

    # Load existing artworks to skip already-fetched IDs
    existing_by_id = {}
    if EXISTING_FILE.exists():
        with open(EXISTING_FILE, "r", encoding="utf-8") as f:
            existing = json.load(f)
        for rec in existing:
            existing_by_id[rec["source_id"]] = rec
        print(f"Loaded {len(existing_by_id)} existing artworks from {EXISTING_FILE.name}")
    print()

    # Initialize session
    print("Fetching main archive page for session...")
    fetch(f"{BASE_URL}/prix/")
    time.sleep(DELAY)

    all_artworks = []  # final combined results
    # Pre-populate with existing records (will be overwritten if re-encountered)
    # We track which IDs we have so detail pages are not re-fetched
    skip_ids = set(existing_by_id.keys())

    for cat_code, cat_label in CATEGORIES:
        print(f"\n{'='*60}")
        print(f"Category: {cat_label} ({cat_code})")
        print(f"{'='*60}")

        # Step 1: Fetch year counts for this category
        try:
            data = fetch_json(f"{BASE_URL}/prix/data/", {"category": cat_code})
        except Exception as e:
            print(f"  ERROR fetching category data: {e}")
            continue
        time.sleep(DELAY)

        year_counts = data.get("aaYearCounts", [])
        total_display = data.get("iTotalDisplayRecords", 0)
        print(f"Found {total_display} works across {len(year_counts)} years")

        if not year_counts:
            print("  No years found, skipping.")
            continue

        for yc in year_counts:
            print(f"  {yc[0]}: {yc[1]} works")

        # Step 2: For each year, fetch work listings
        cat_works = []
        seen_ids = set()

        for year_str, count in year_counts:
            year = int(year_str)
            print(f"\n  Fetching {year} ({count} works)...")

            try:
                year_html = fetch(f"{BASE_URL}/prix/data/year/", {
                    "year": year,
                    "category": cat_code,
                })
            except Exception as e:
                print(f"    ERROR fetching year {year}: {e}")
                continue
            time.sleep(DELAY)

            works = parse_year_html(year_html)
            print(f"    Parsed {len(works)} works from HTML")

            for w in works:
                if w["source_id"] in seen_ids:
                    continue
                seen_ids.add(w["source_id"])
                w["year"] = year
                w["category_code"] = cat_code
                cat_works.append(w)

            if len(works) != count:
                print(f"    WARNING: Expected {count}, got {len(works)}")

        print(f"\n  Total works from listings: {len(cat_works)}")

        # Step 3: Fetch detail pages (skip IDs already in existing data)
        new_count = 0
        skipped_count = 0

        for i, work in enumerate(cat_works):
            wid = work["source_id"]

            if wid in skip_ids:
                # Already have this work -- carry existing record forward
                skipped_count += 1
                if wid in existing_by_id:
                    all_artworks.append(existing_by_id[wid])
                continue

            skip_ids.add(wid)
            new_count += 1
            print(f"    [{i+1}/{len(cat_works)}] Fetching detail for {wid}: {work['title'][:40]}...")

            try:
                detail_html = fetch(f"{BASE_URL}/prix/{wid}/")
                detail = parse_detail_page(detail_html, wid)
            except Exception as e:
                print(f"      ERROR fetching detail: {e}")
                detail = {}

            time.sleep(DELAY)

            default_medium = MEDIUM_MAP.get(cat_code, "Digital art")
            record = {
                "source": "ars-electronica",
                "source_id": wid,
                "source_url": f"https://archive.aec.at/prix/{wid}/",
                "title": detail.get("title", work["title"]),
                "artist": detail.get("artist", work["artist"]),
                "year": detail.get("year", work["year"]),
                "url": detail.get("url", ""),
                "medium": default_medium,
                "award": detail.get("award", work["award"]),
                "category": detail.get("category", cat_label),
                "category_code": cat_code,
                "description": detail.get("description", ""),
                "technologies": [],
                "preservation": {"status": "unknown"},
            }
            all_artworks.append(record)

        print(f"\n  {cat_label}: {new_count} new, {skipped_count} skipped (already fetched)")

    # Also add any existing records that were not encountered in the listing
    # (in case the existing file has IDs not re-encountered above)
    existing_ids_in_result = {r["source_id"] for r in all_artworks}
    carried = 0
    for sid, rec in existing_by_id.items():
        if sid not in existing_ids_in_result:
            all_artworks.append(rec)
            carried += 1
    if carried:
        print(f"\nCarried forward {carried} existing records not found in category listings")

    # Deduplicate by source_id (keep first occurrence)
    deduped = {}
    for r in all_artworks:
        if r["source_id"] not in deduped:
            deduped[r["source_id"]] = r
    all_artworks = list(deduped.values())

    # Sort by year then title
    all_artworks.sort(key=lambda r: (r.get("year", 9999), r.get("title", "")))

    # Save output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_artworks, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(all_artworks)} artworks to {OUTPUT_FILE}")

    # Summary stats
    print("\n--- Summary ---")

    cats = {}
    for a in all_artworks:
        c = a.get("category_code", a.get("category", "?"))
        cats[c] = cats.get(c, 0) + 1
    print("\nCategory breakdown:")
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count}")

    awards = {}
    for a in all_artworks:
        awards[a["award"]] = awards.get(a["award"], 0) + 1
    print("\nAward breakdown:")
    for award, count in sorted(awards.items()):
        print(f"  {award}: {count}")

    years = {}
    for a in all_artworks:
        years[a["year"]] = years.get(a["year"], 0) + 1
    print("\nYear breakdown:")
    for year, count in sorted(years.items()):
        print(f"  {year}: {count}")

    with_url = sum(1 for a in all_artworks if a["url"])
    with_desc = sum(1 for a in all_artworks if a["description"])
    print(f"\nWith project URL: {with_url}/{len(all_artworks)}")
    print(f"With description: {with_desc}/{len(all_artworks)}")


if __name__ == "__main__":
    main()
