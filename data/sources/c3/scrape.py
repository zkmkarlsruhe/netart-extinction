#!/usr/bin/env python3
"""Scrape artworks from the C3 Foundation Budapest collection."""

import json
import re
import time
import urllib.request
from html import unescape
from html.parser import HTMLParser

BASE_URL = "https://www.c3.hu"
INDEX_URL = f"{BASE_URL}/collection/index_en.php"
SOURCE_URL = "https://www.c3.hu/collection/"
DELAY = 0.5
UA = "Mozilla/5.0 (compatible; research bot)"


def fetch(url, retries=2):
    """Fetch a URL, falling back to Wayback Machine on failure."""
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            resp = urllib.request.urlopen(req, timeout=20)
            raw = resp.read()
            # Try iso-8859-1 first (what the English pages declare), fall back to utf-8
            for enc in ("iso-8859-1", "utf-8", "windows-1250"):
                try:
                    return raw.decode(enc)
                except UnicodeDecodeError:
                    continue
            return raw.decode("utf-8", errors="replace")
        except Exception as e:
            if attempt < retries:
                print(f"  Retry {attempt+1} for {url}: {e}")
                time.sleep(1)
            else:
                # Try Wayback Machine
                wb_url = f"https://web.archive.org/web/2024/{url}"
                print(f"  Trying Wayback Machine: {wb_url}")
                try:
                    req = urllib.request.Request(wb_url, headers={"User-Agent": UA})
                    resp = urllib.request.urlopen(req, timeout=20)
                    return resp.read().decode("utf-8", errors="replace")
                except Exception as e2:
                    print(f"  Wayback also failed: {e2}")
                    return None


def strip_tags(html_str):
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", "", html_str)
    text = unescape(text)
    return text.strip()


def parse_index(html):
    """Extract project IDs and titles from the index page sidebar."""
    # Match links like: index_en.php?id=22
    pattern = r'index_en\.php\?id=(\d+)"[^>]*>([^<]+)<'
    matches = re.findall(pattern, html)
    # Deduplicate by ID (links appear in both main sidebar and detail sidebar)
    seen = set()
    projects = []
    for pid, title in matches:
        if pid not in seen:
            seen.add(pid)
            projects.append((pid, unescape(title).strip()))
    return projects


def parse_detail(html, pid):
    """Parse a detail page for artist, title, and year."""
    result = {"title": None, "artist": None, "year": None}

    # Find the content table (width="500")
    content_start = html.find('<table width="500"')
    if content_start == -1:
        return result
    content = html[content_start:]

    # Title: inside div with dotted border
    title_match = re.search(
        r'border-color:#ff0000[^>]*>([^<]+)<', content
    )
    if title_match:
        result["title"] = unescape(title_match.group(1)).strip()

    # Artist: in the first <td> with font-size:11px, inside <p> or <b> tags
    # Pattern 1: <b>LastName</b> FirstName (e.g., <b>Szegedy-Maszák</b> Zoltán)
    # Pattern 2: <b>ArtistName</b><br> (group/pseudonym)
    # Pattern 3: Just text in a <p> tag
    artist_section = content[:content.find('border-color:#ff0000')]

    # Try pattern: <b>LastName</b> FirstName
    artist_match = re.search(
        r'<p[^>]*>\s*<b>([^<]+)</b>\s*([^<]*?)\s*</p>',
        artist_section
    )
    if artist_match:
        last_name = unescape(artist_match.group(1)).strip()
        first_name = unescape(artist_match.group(2)).strip()
        if last_name == "&nbsp;" or last_name == "\xa0" or not last_name.strip():
            result["artist"] = None
        elif first_name:
            result["artist"] = f"{first_name} {last_name}"
        else:
            result["artist"] = last_name
    else:
        # Try simpler pattern
        artist_match2 = re.search(
            r'font-size:11px[^>]*><p[^>]*>(.+?)</p>',
            artist_section, re.DOTALL
        )
        if artist_match2:
            raw = strip_tags(artist_match2.group(1)).strip()
            if raw and raw != "\xa0":
                result["artist"] = raw

    # Year: standalone 4-digit number in a table cell
    year_match = re.search(
        r'<td[^>]*style="font-size:11px;"[^>]*><b>(\d{4})</b></td>',
        content
    )
    if year_match:
        result["year"] = int(year_match.group(1))

    # Also try to find subtitle line (e.g., "a VRML project by ...")
    subtitle_match = re.search(
        r'<td[^>]*style="font-size:11px;"[^>]*><b>([^<]*(?:project|installation|work)[^<]*)</b></td>',
        content, re.IGNORECASE
    )

    return result


def main():
    print("Fetching C3 collection index...")
    index_html = fetch(INDEX_URL)
    if not index_html:
        print("ERROR: Could not fetch index page")
        return

    projects = parse_index(index_html)
    print(f"Found {len(projects)} projects in index")

    artworks = []
    for i, (pid, index_title) in enumerate(projects):
        detail_url = f"{INDEX_URL}?id={pid}"
        print(f"[{i+1}/{len(projects)}] Fetching id={pid}: {index_title}")

        time.sleep(DELAY)
        detail_html = fetch(detail_url)

        if not detail_html:
            print(f"  SKIP: could not fetch")
            continue

        info = parse_detail(detail_html, pid)

        # Use detail page title if found, otherwise fall back to index title
        title = info["title"] or index_title

        artwork = {
            "source": "c3",
            "source_url": SOURCE_URL,
            "title": title,
            "artist": info["artist"],
            "year": info["year"],
            "url": f"https://www.c3.hu/collection/index_en.php?id={pid}",
            "medium": "Net art",
        }
        artworks.append(artwork)
        print(f"  -> {artwork['title']} | {artwork['artist']} | {artwork['year']}")

    # Sort by year (None last), then title
    artworks.sort(key=lambda a: (a["year"] or 9999, a["title"] or ""))

    out_path = "/x/coding/netart-extinction/data/sources/c3/artworks.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(artworks)} artworks to {out_path}")

    # Summary stats
    with_year = sum(1 for a in artworks if a["year"])
    with_artist = sum(1 for a in artworks if a["artist"])
    print(f"  With year: {with_year}/{len(artworks)}")
    print(f"  With artist: {with_artist}/{len(artworks)}")
    if with_year:
        years = [a["year"] for a in artworks if a["year"]]
        print(f"  Year range: {min(years)}-{max(years)}")


if __name__ == "__main__":
    main()
