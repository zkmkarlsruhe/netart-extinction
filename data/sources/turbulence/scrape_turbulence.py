#!/usr/bin/env python3
"""
Scrape Turbulence.org commissioned artworks from Wayback Machine.

Strategy:
1. Use CDX API to find captured archive page URLs
2. Fetch each yearly archive page (96.html through 14.html)
3. Also use CDX to get project page slugs as supplementary title list
4. Parse for artwork titles, artists, years, URLs
5. Append to existing artworks.json, dedup by title
"""

import json
import html as html_mod
import os
import re
import time
import urllib.request
import urllib.error

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(DATA_DIR, "artworks.json")

WAYBACK_CDX = "https://web.archive.org/cdx/search/cdx"
WAYBACK_BASE = "https://web.archive.org/web"

DELAY = 2.5  # seconds between Wayback requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (research bot; net art preservation project)"
}

# Known noise links to skip from archive pages
NOISE = {
    "home", "about", "contact", "archives", "back", "next", "previous",
    "read bio", ">>", "&gt;&gt;", "bio", "turbulence.org", "new radio",
    "commissions", "artists' studios", "guest curators", "spotlight",
    "events", "here", "facebook", "website", "second life", "layar",
    "cbsnews.com", "read an analysis >>", "read an interview >>",
    "read a review >>", "read /1/review >>", "read /2/review >>",
    "read 1/interview >>", "read 2/interview", "winners announced",
    "committee", "yeas and nays", "world premiere", "live streamed",
    "new radio and performing arts, inc.", "turbulence",
}

# Known venue/org names (not artworks)
VENUES = {
    "art interactive", "upgrade! boston", "upgrade! international",
    "eyebeam art & technology center", "issue project room",
    "dunn and brown contemporary", "judi rotenberg gallery",
    "museum of science", "fred jones museum of art",
    "cambridge science fesitval", "emerson college",
    "harvestworks", "pace digital gallery",
    "boston cyberarts festival", "eyebeam art & technology center's project space",
}

# Wayback chrome noise
WAYBACK_NOISE = {
    "about this capture", "alexa crawls", "alexa internet",
    "wayback machine", "internet archive", "electronic literature organization",
    "electronic literature: collections of works",
    "wide crawl started september 2012", "fix all broken links on the web",
    "wikipedia near real time (from irc)", "rid the web of broken links",
}


def fetch_url(url, retries=3, backoff=15):
    """Fetch URL with retries and exponential backoff for rate limiting."""
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                wait = backoff * (2 ** attempt)
                print(f"  Rate limited ({e.code}), waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 404:
                print(f"  404: {url}")
                return None
            else:
                print(f"  HTTP {e.code}: {url}")
                if attempt < retries - 1:
                    time.sleep(backoff)
                else:
                    return None
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < retries - 1:
                time.sleep(backoff)
            else:
                return None
    return None


def cdx_search(url_pattern, extra_params=""):
    """Use Wayback CDX API to find captured URLs."""
    params = f"?url={url_pattern}&output=json&fl=timestamp,original,statuscode&collapse=urlkey{extra_params}"
    cdx_url = WAYBACK_CDX + params
    print(f"CDX query: {cdx_url}")
    text = fetch_url(cdx_url)
    if not text:
        return []
    try:
        rows = json.loads(text)
        return rows[1:] if len(rows) > 1 else []
    except json.JSONDecodeError:
        print("  Failed to parse CDX response")
        return []


def is_noise(title):
    """Check if a title is navigation noise, not an artwork."""
    t = title.lower().strip()
    if t in NOISE or t in WAYBACK_NOISE or t in VENUES:
        return True
    # Pure numbers (year navigation like "01", "99")
    if re.match(r'^\d{1,2}$', t):
        return True
    # Wayback-specific patterns
    if 'captures' in t or 'alexa' in t.lower():
        return True
    if re.match(r'^\d+ captures$', t):
        return True
    # Very short or starts with special chars only
    if len(t) < 2:
        return True
    return False


def extract_links_from_html(html_text):
    """Extract all <a> tags with href and text using regex (more robust than HTMLParser for messy HTML)."""
    links = []
    # Match <a...href="..."...>text</a>
    pattern = re.compile(r'<a\s[^>]*href\s*=\s*["\']([^"\']*)["\'][^>]*>(.*?)</a>', re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(html_text):
        href = m.group(1).strip()
        # Strip inner HTML tags from link text
        text = re.sub(r'<[^>]+>', ' ', m.group(2))
        text = html_mod.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and href:
            links.append((text, href))
    return links


def parse_archive_page(html_text, source_url, year):
    """Parse an archive page and extract artwork entries."""
    works = []
    links = extract_links_from_html(html_text)

    seen_titles = set()
    for title, href in links:
        if is_noise(title):
            continue

        # Skip navigation links (relative links to other archive pages)
        if re.match(r'^/?(?:\d{2}\.html|archives/\d{2}\.html)$', href):
            continue

        # Skip pure Wayback infrastructure URLs
        if 'web.archive.org' in href and '/web/' not in href:
            continue
        if href.startswith('//web.archive.org'):
            continue
        if 'alexa.com' in href:
            continue

        # Normalize title
        title = re.sub(r'\s+', ' ', title).strip()

        # Skip if already seen
        title_key = title.lower()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)

        works.append({
            "source": "turbulence",
            "source_url": source_url,
            "title": title,
            "artist": "",
            "year": year,
            "url": href,
            "medium": "Net art",
            "technologies": [],
            "preservation": {"status": "unknown"}
        })

    return works


def try_extract_artist_from_context(html_text, title):
    """Try to find artist name near a title in the archive page HTML."""
    # Look for pattern: title followed by artist name or "by artist"
    escaped_title = re.escape(title)
    # Pattern: title...artist name (in bold, span, or after "by")
    patterns = [
        escaped_title + r'.*?(?:by\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        escaped_title + r'.*?<(?:b|strong|em)>([^<]+)</(?:b|strong|em)>',
    ]
    for pat in patterns:
        m = re.search(pat, html_text, re.DOTALL)
        if m:
            artist = m.group(1).strip()
            if len(artist) > 3 and len(artist) < 60:
                return artist
    return ""


def scrape_archive_pages():
    """Scrape yearly archive pages from Wayback Machine."""
    all_works = []

    print("=== Phase 1: CDX lookup for archive pages ===")
    cdx_results = cdx_search("turbulence.org/archives/*")
    time.sleep(DELAY)

    # Build map of archive page -> best wayback URL (prefer later captures)
    archive_captures = {}
    for row in cdx_results:
        timestamp, original, status = row[0], row[1], row[2]
        if status != "200":
            continue
        m = re.search(r'/archives/(\d+\.html)', original)
        if m:
            page = m.group(1)
            # Prefer captures from 2013-2019 (more complete pages)
            if page not in archive_captures or timestamp > archive_captures[page][0]:
                archive_captures[page] = (timestamp, original)

    print(f"  Found {len(archive_captures)} archive pages in CDX")

    # Also try to get better (later) captures specifically
    cdx_results2 = cdx_search("turbulence.org/archives/*", "&from=20130101&to=20200101")
    time.sleep(DELAY)
    for row in cdx_results2:
        timestamp, original, status = row[0], row[1], row[2]
        if status != "200":
            continue
        m = re.search(r'/archives/(\d+\.html)', original)
        if m:
            page = m.group(1)
            if page not in archive_captures or timestamp > archive_captures[page][0]:
                archive_captures[page] = (timestamp, original)

    # Year pages: 96.html through 14.html
    year_pages = {}
    for yr in range(96, 100):
        year_pages[f"{yr:02d}.html"] = 1900 + yr
    for yr in range(0, 15):
        year_pages[f"{yr:02d}.html"] = 2000 + yr

    for page, year in sorted(year_pages.items(), key=lambda x: x[1]):
        print(f"\n--- {page} (year {year}) ---")

        if page in archive_captures:
            ts, orig = archive_captures[page]
            url = f"{WAYBACK_BASE}/{ts}/{orig}"
        else:
            url = f"{WAYBACK_BASE}/2019/https://turbulence.org/archives/{page}"

        print(f"  Fetching: {url}")
        html_text = fetch_url(url)
        time.sleep(DELAY)

        if not html_text:
            print(f"  No content for {page}")
            continue

        works = parse_archive_page(html_text, f"https://turbulence.org/archives/{page}", year)
        print(f"  Found {len(works)} works:")
        for w in works:
            print(f"    - {w['title']}")
        all_works.extend(works)

    return all_works


def get_project_titles_from_cdx():
    """Get project titles from CDX slug list (no individual page fetches needed)."""
    print("\n=== Phase 2: Project titles from CDX slugs ===")
    cdx_results = cdx_search("turbulence.org/project/*", "&limit=500")
    time.sleep(DELAY)

    slugs = set()
    for row in cdx_results:
        timestamp, original, status = row[0], row[1], row[2]
        if status != "200":
            continue
        m = re.search(r'/project/([^/?#]+)/?$', original)
        if m:
            slug = m.group(1)
            if slug not in ("page", "feed", "category", "tag", "embed"):
                slugs.add(slug)

    print(f"  Found {len(slugs)} unique project slugs")

    # Convert slugs to rough titles (for dedup matching with archive page data)
    titles = []
    for slug in sorted(slugs):
        # Convert slug to title: replace hyphens with spaces, title case
        title = slug.replace('-', ' ').replace('_', ' ')
        # Don't title-case - keep raw for matching
        titles.append({
            "slug": slug,
            "title_from_slug": title,
            "url": f"https://turbulence.org/project/{slug}/"
        })

    return titles


def deduplicate(works):
    """Deduplicate works by normalized title."""
    seen = {}
    unique = []
    for w in works:
        key = re.sub(r'\s+', ' ', w["title"]).strip().lower()
        # Also normalize common variations
        key = key.replace('\n', ' ').replace('\r', '')
        key = re.sub(r'\s+', ' ', key).strip()

        if key in seen:
            existing = seen[key]
            # Merge: prefer entries with more info
            if not existing.get("artist") and w.get("artist"):
                existing["artist"] = w["artist"]
            if not existing.get("year") and w.get("year"):
                existing["year"] = w["year"]
            if existing.get("url", "").startswith("/") and not w.get("url", "").startswith("/"):
                existing["url"] = w["url"]
            continue
        seen[key] = w
        unique.append(w)
    return unique


def clean_works(works):
    """Post-process and clean up work entries."""
    cleaned = []
    for w in works:
        title = w["title"]

        # Remove HTML entities that weren't decoded
        title = html_mod.unescape(title)

        # Clean up whitespace
        title = re.sub(r'\s+', ' ', title).strip()

        # Skip entries that are clearly not artworks after cleaning
        if is_noise(title):
            continue

        # Skip entries that look like artist-only pages without artwork title
        # (single names like "kanarek", "arcangel" etc.)
        # But keep compound names and titled works
        if re.match(r'^[a-z]+$', title) and len(title) < 20:
            continue

        w["title"] = title
        cleaned.append(w)

    return cleaned


def main():
    # Load existing data
    existing = []
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            existing = json.load(f)
        print(f"Loaded {len(existing)} existing works\n")

    # Phase 1: Scrape archive pages
    archive_works = scrape_archive_pages()

    # Phase 2: Get project slugs from CDX (lightweight, no page fetches)
    project_info = get_project_titles_from_cdx()

    # Clean archive works
    archive_works = clean_works(archive_works)

    print(f"\n=== Results ===")
    print(f"Existing works: {len(existing)}")
    print(f"Works from archive pages: {len(archive_works)}")
    print(f"Project slugs from CDX: {len(project_info)}")

    # Combine existing + new archive page works
    combined = existing + archive_works
    combined = deduplicate(combined)

    # Now check which project slugs aren't represented
    existing_titles = {re.sub(r'\s+', ' ', w["title"]).strip().lower() for w in combined}

    new_from_slugs = 0
    for p in project_info:
        slug_title = p["title_from_slug"].lower()
        # Check if any existing title contains this slug title or vice versa
        found = False
        for et in existing_titles:
            if slug_title in et or et in slug_title:
                found = True
                break
            # Also check with spaces removed
            if slug_title.replace(' ', '') in et.replace(' ', ''):
                found = True
                break

        if not found and len(slug_title) > 3:
            # Capitalize properly
            nice_title = p["title_from_slug"].title()
            combined.append({
                "source": "turbulence",
                "source_url": p["url"],
                "title": nice_title,
                "artist": "",
                "year": None,
                "url": p["url"],
                "medium": "Net art",
                "technologies": [],
                "preservation": {"status": "unknown"}
            })
            new_from_slugs += 1
            print(f"  New from slug: {nice_title}")

    combined = deduplicate(combined)

    print(f"\nNew works added from slugs: {new_from_slugs}")
    print(f"Final total after dedup: {len(combined)}")

    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(combined)} works to {OUTPUT_FILE}")

    # Stats
    years = {}
    for w in combined:
        y = w.get("year")
        if y:
            years[y] = years.get(y, 0) + 1
    print("\nWorks by year:")
    for y in sorted(years):
        print(f"  {y}: {years[y]}")

    no_year = sum(1 for w in combined if not w.get("year"))
    print(f"  No year: {no_year}")


if __name__ == "__main__":
    main()
