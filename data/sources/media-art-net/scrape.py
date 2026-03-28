#!/usr/bin/env python3
"""
Scraper for Media Art Net (medienkunstnetz.de).

Fetches the alphabetical works index pages to collect all work slugs,
then visits each work's detail page to extract title, artist, year,
medium/category, and URL.

Uses only stdlib. Polite: 1.5s delay between requests.
Retries failed requests up to 3 times with backoff.
Saves progress incrementally so interrupted runs can be resumed.

Output: data/sources/media-art-net/artworks.json
"""

import json
import os
import re
import sys
import time
import html as html_module
import urllib.request

BASE = "http://www.medienkunstnetz.de"
INDEX_URL = BASE + "/index/works/{}/"
LETTERS = ["%23"] + [chr(c) for c in range(ord("a"), ord("z") + 1)]
HEADERS = {"User-Agent": "Mozilla/5.0 (net art preservation research project)"}
DELAY = 1.5
MAX_RETRIES = 3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(SCRIPT_DIR, "artworks.json")
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "progress.json")


def log(msg):
    print(msg, flush=True)


def fetch(url, retries=MAX_RETRIES):
    """Fetch a URL and return decoded text. Retries on failure."""
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            resp = urllib.request.urlopen(req, timeout=20)
            return resp.read().decode("iso-8859-1", errors="replace")
        except Exception as e:
            if attempt < retries - 1:
                wait = DELAY * (2 ** attempt)
                log(f"    Retry {attempt+1}/{retries-1} after {wait}s: {e}")
                time.sleep(wait)
            else:
                log(f"    FAILED after {retries} attempts: {e}")
                return None


def extract_slugs_from_index(html_text):
    """Extract work slugs from an index page.
    Links look like: openMknWin('/works/SLUG/',2)
    """
    pattern = r"openMknWin\('/works/([^']+)/',\s*2\)"
    return list(dict.fromkeys(re.findall(pattern, html_text)))


def decode_html_entities(text):
    """Decode HTML entities like &laquo; &ndash; &#39; etc."""
    text = html_module.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_detail_page(html_text, slug):
    """Extract artwork metadata from a detail page."""
    result = {}

    # --- Title and artist from <title> tag ---
    # Format: "Media Art Net | Artist: Title"
    title_match = re.search(r"<title>Media Art Net \| (.+?)</title>", html_text)
    if title_match:
        raw = decode_html_entities(title_match.group(1))
        if ": " in raw:
            artist_part, title_part = raw.split(": ", 1)
            result["artist"] = artist_part.strip()
            result["title"] = title_part.strip()
        else:
            result["title"] = raw
            result["artist"] = None
    else:
        result["title"] = slug
        result["artist"] = None

    # --- Year from caption div ---
    caption_match = re.search(
        r'<div id="caption"[^>]*>\s*<strong>(.*?)</strong>', html_text, re.DOTALL
    )
    year = None
    year_display = None
    if caption_match:
        caption = decode_html_entities(caption_match.group(1))
        year_match = re.search(r"(\d{4})\s*[-/\u2013]\s*(\d{4})", caption)
        if year_match:
            year = int(year_match.group(1))
            year_display = f"{year_match.group(1)}-{year_match.group(2)}"
        else:
            year_match = re.search(r"\b(1[89]\d{2}|20[0-2]\d)\b", caption)
            if year_match:
                year = int(year_match.group(1))
    result["year"] = year
    if year_display:
        result["year_display"] = year_display

    # --- Categories (medium) from related section ---
    cat_match = re.search(
        r"<strong>Categories:</strong>\s*(.*?)</p>", html_text, re.DOTALL
    )
    if cat_match:
        cats = re.findall(r'class="text">([^<]+)</a>', cat_match.group(1))
        cats = [decode_html_entities(c) for c in cats]
        result["medium"] = ", ".join(cats) if cats else None
    else:
        rel2_match = re.search(
            r'<div class="finder" id="related2"><div class="rel">(.*?)</div>',
            html_text,
            re.DOTALL,
        )
        if rel2_match:
            medium_raw = decode_html_entities(rel2_match.group(1))
            result["medium"] = medium_raw if medium_raw else None
        else:
            result["medium"] = None

    # --- Keywords ---
    kw_match = re.search(
        r"<strong>Keywords:</strong>\s*(.*?)</p>", html_text, re.DOTALL
    )
    if kw_match:
        kws = re.findall(r'class="text">([^<]+)</a>', kw_match.group(1))
        kws = [decode_html_entities(k) for k in kws]
        result["keywords"] = kws if kws else None
    else:
        result["keywords"] = None

    return result


def load_progress():
    """Load progress from a previous interrupted run."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"done_slugs": [], "artworks": []}


def save_progress(done_slugs, artworks):
    """Save progress for resume capability."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump({"done_slugs": done_slugs, "artworks": artworks}, f, ensure_ascii=False)


def main():
    # Load any previous progress
    progress = load_progress()
    done_set = set(progress["done_slugs"])
    artworks = progress["artworks"]
    if done_set:
        log(f"Resuming: {len(done_set)} works already fetched, {len(artworks)} artworks collected")

    # Step 1: Collect all work slugs from alphabetical index pages
    log("=== Collecting work slugs from index pages ===")
    all_slugs = []
    for letter in LETTERS:
        url = INDEX_URL.format(letter)
        log(f"  Fetching index: {letter} -> {url}")
        html_text = fetch(url)
        if html_text:
            slugs = extract_slugs_from_index(html_text)
            log(f"    Found {len(slugs)} works")
            all_slugs.extend(slugs)
        time.sleep(DELAY)

    # Deduplicate while preserving order
    seen = set()
    unique_slugs = []
    for s in all_slugs:
        if s not in seen:
            seen.add(s)
            unique_slugs.append(s)

    log(f"\nTotal unique works found: {len(unique_slugs)}")
    remaining = [s for s in unique_slugs if s not in done_set]
    log(f"Remaining to fetch: {len(remaining)}")

    # Step 2: Fetch each work's detail page
    log("\n=== Fetching work detail pages ===")
    total = len(unique_slugs)
    for i, slug in enumerate(unique_slugs):
        if slug in done_set:
            continue

        work_url = f"{BASE}/works/{slug}/"
        log(f"  [{i+1}/{total}] {slug}")
        html_text = fetch(work_url)
        if html_text is None:
            log(f"    SKIPPED (fetch failed)")
            done_set.add(slug)
            progress["done_slugs"].append(slug)
            time.sleep(DELAY)
            continue

        info = parse_detail_page(html_text, slug)

        artwork = {
            "source": "media-art-net",
            "source_url": "http://www.medienkunstnetz.de/works/",
            "title": info["title"],
            "artist": info["artist"],
            "year": info["year"],
            "url": work_url,
            "medium": info["medium"],
        }
        if info.get("year_display"):
            artwork["year_display"] = info["year_display"]
        if info.get("keywords"):
            artwork["keywords"] = info["keywords"]

        artworks.append(artwork)
        done_set.add(slug)
        progress["done_slugs"].append(slug)

        # Save progress every 50 works
        if len(done_set) % 50 == 0:
            save_progress(progress["done_slugs"], artworks)
            log(f"    [progress saved: {len(artworks)} artworks]")

        time.sleep(DELAY)

    # Step 3: Write final output
    log(f"\n=== Writing {len(artworks)} artworks to {OUTPUT} ===")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    # Clean up progress file
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

    log("Done!")


if __name__ == "__main__":
    main()
