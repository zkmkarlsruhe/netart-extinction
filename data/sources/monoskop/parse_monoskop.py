#!/usr/bin/env python3
"""
Parse Monoskop wiki pages to extract net art works, artists, and related data.
Saves normalized artwork data to artworks.json.
"""

import json
import os
import re
from html import unescape

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
OUT_FILE = os.path.join(os.path.dirname(__file__), "artworks.json")

def strip_tags(html_str):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '', html_str)
    return unescape(text).strip()

def extract_first_url(html_str):
    """Extract first external URL from HTML fragment."""
    m = re.search(r'href="(https?://[^"]+)"', html_str)
    return m.group(1) if m else None

def parse_works_table(html):
    """Parse the 'Works in public collections' table from Net_art page."""
    artworks = []
    works_match = re.search(
        r'id="Works_in_public_collections".*?</h2>(.*?)(?=<h2>|$)',
        html, re.DOTALL
    )
    if not works_match:
        return artworks

    table_html = works_match.group(1)
    # Split into rows, skip header
    rows = re.split(r'<tr\b[^>]*>', table_html)[2:]  # skip table tag and header row

    for row in rows:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(cells) < 9:
            continue

        artist = strip_tags(cells[0]).strip()
        # cells[1] = country
        title_cell = cells[2]
        year_raw = strip_tags(cells[3]).strip()
        collection = strip_tags(cells[4]).strip()
        # cells[5] = acquisition year
        # cells[6] = collection number
        # cells[7] = collection URL
        medium = strip_tags(cells[8]).strip()

        # Extract title
        title = strip_tags(title_cell).strip()
        # Extract URL from title cell
        url = extract_first_url(title_cell)

        # Parse year - take first 4-digit year
        year = None
        year_m = re.search(r'(\d{4})', year_raw)
        if year_m:
            year = int(year_m.group(1))

        if not title:
            continue

        artworks.append({
            "source": "monoskop",
            "source_url": "https://monoskop.org/Net_art#Works_in_public_collections",
            "title": title,
            "artist": artist,
            "year": year,
            "url": url,
            "medium": medium or "Net art",
            "collection": collection,
        })

    return artworks


def parse_software_art_works(html):
    """Parse works from Software_art page list items."""
    artworks = []
    works_match = re.search(
        r'id="Works".*?</h2>(.*?)(?=<h2>)',
        html, re.DOTALL
    )
    if not works_match:
        return artworks

    section = works_match.group(1)
    items = re.findall(r'<li>(.*?)</li>', section, re.DOTALL)

    for item in items:
        text = strip_tags(item)
        url = extract_first_url(item)

        # Typical pattern: "Artist, Title, Year. Description"
        # Try to extract italic title: <i>...</i> or <i><a ...>...</a></i>
        title_match = re.search(r'<i[^>]*>(.*?)</i>', item, re.DOTALL)
        title = strip_tags(title_match.group(1)) if title_match else None

        # Extract year
        year = None
        year_m = re.search(r'(\d{4})', text)
        if year_m:
            year = int(year_m.group(1))

        # Artist is typically text before the first comma or before <i>
        artist = None
        if title_match:
            before_title = item[:title_match.start()]
            artist = strip_tags(before_title).rstrip(', ').strip()
        else:
            # Try first part before comma
            parts = text.split(',', 1)
            if len(parts) > 1:
                artist = parts[0].strip()

        if not title and not artist:
            continue

        # If we couldn't find an italic title, try the text after artist
        if not title:
            parts = text.split(',', 2)
            if len(parts) > 1:
                title = parts[1].strip().rstrip('.')

        if not title:
            continue

        artworks.append({
            "source": "monoskop",
            "source_url": "https://monoskop.org/Software_art#Works",
            "title": title,
            "artist": artist or "Unknown",
            "year": year,
            "url": url,
            "medium": "Software art",
        })

    return artworks


def parse_exhibitions_as_platforms(html):
    """Parse the 'Digital exhibitions, platforms, archives' section for notable platforms/artworks."""
    artworks = []
    exh_match = re.search(
        r'id="Digital_exhibitions.*?".*?</h2>(.*?)(?=<h2>)',
        html, re.DOTALL
    )
    if not exh_match:
        return artworks

    section = exh_match.group(1)
    items = re.findall(r'<li>(.*?)</li>', section, re.DOTALL)

    for item in items:
        text = strip_tags(item)
        # Get first external link as the main URL and title
        link_match = re.search(
            r'<a[^>]*class="external text"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>',
            item
        )
        if not link_match:
            continue

        url = link_match.group(1)
        title = unescape(link_match.group(2)).strip()

        # Try to extract year
        year = None
        year_m = re.search(r'(\d{4})', text)
        if year_m:
            year = int(year_m.group(1))

        # Try to extract curator/creator
        artist = None
        # Common patterns: "by X", "Curated by X", "Run by X", "Created by X"
        for pattern in [
            r'(?:Curated|Created|Run|Launched|Initiated|Developed) by ([^,\.]+)',
            r'by ([A-Z][a-z]+ [A-Z][a-z]+)',
        ]:
            m = re.search(pattern, text)
            if m:
                artist = m.group(1).strip()
                break

        artworks.append({
            "source": "monoskop",
            "source_url": "https://monoskop.org/Net_art#Digital_exhibitions,_platforms,_archives",
            "title": title,
            "artist": artist,
            "year": year,
            "url": url,
            "medium": "Net art platform/exhibition",
        })

    return artworks


def parse_artist_list(html, page_name, medium):
    """Parse artist lists (internal wiki links) from a section."""
    artists = []
    artists_match = re.search(
        r'id="Artists.*?".*?</h2>(.*?)(?=<h2>)',
        html, re.DOTALL
    )
    if not artists_match:
        return artists

    section = artists_match.group(1)
    links = re.findall(
        r'<a href="(/[^"]+)"[^>]*title="([^"]+)"[^>]*>([^<]+)</a>',
        section
    )

    for href, title_attr, display_text in links:
        name = unescape(display_text).strip()
        if name and not name.startswith('File:'):
            artists.append({
                "name": name,
                "monoskop_url": f"https://monoskop.org{href}",
                "medium": medium,
            })

    return artists


def parse_glitch_art_artists(html):
    """Parse artist/page links from Glitch_art."""
    artists = []
    pages_match = re.search(
        r'id="Pages".*?</h2>(.*?)(?=<h2>)',
        html, re.DOTALL
    )
    if not pages_match:
        return artists

    section = pages_match.group(1)
    links = re.findall(
        r'<a href="(/[^"]+)"[^>]*title="([^"]+)"[^>]*>([^<]+)</a>',
        section
    )

    for href, title_attr, display_text in links:
        name = unescape(display_text).strip()
        if name:
            artists.append({
                "name": name,
                "monoskop_url": f"https://monoskop.org{href}",
                "medium": "Glitch art",
            })

    return artists


def main():
    all_artworks = []
    all_artists = []

    # --- Net_art page ---
    net_art_path = os.path.join(RAW_DIR, "Net_art.html")
    if os.path.exists(net_art_path):
        with open(net_art_path) as f:
            html = f.read()

        # Works in public collections (structured table)
        works = parse_works_table(html)
        all_artworks.extend(works)
        print(f"Net_art - Works in public collections: {len(works)}")

        # Digital exhibitions/platforms
        platforms = parse_exhibitions_as_platforms(html)
        all_artworks.extend(platforms)
        print(f"Net_art - Digital exhibitions/platforms: {len(platforms)}")

        # Artist list
        artists = parse_artist_list(html, "Net_art", "Net art")
        all_artists.extend(artists)
        print(f"Net_art - Artists: {len(artists)}")

    # --- Software_art page ---
    sw_art_path = os.path.join(RAW_DIR, "Software_art.html")
    if os.path.exists(sw_art_path):
        with open(sw_art_path) as f:
            html = f.read()

        works = parse_software_art_works(html)
        all_artworks.extend(works)
        print(f"Software_art - Works: {len(works)}")

        artists = parse_artist_list(html, "Software_art", "Software art")
        all_artists.extend(artists)
        print(f"Software_art - Artists: {len(artists)}")

    # --- Glitch_art page ---
    glitch_path = os.path.join(RAW_DIR, "Glitch_art.html")
    if os.path.exists(glitch_path):
        with open(glitch_path) as f:
            html = f.read()

        artists = parse_glitch_art_artists(html)
        all_artists.extend(artists)
        print(f"Glitch_art - Artists/pages: {len(artists)}")

    # Deduplicate artworks by (title, artist)
    seen = set()
    unique_artworks = []
    for aw in all_artworks:
        key = ((aw.get("title") or "").lower(), (aw.get("artist") or "").lower())
        if key not in seen:
            seen.add(key)
            unique_artworks.append(aw)

    print(f"\nTotal unique artworks: {len(unique_artworks)}")
    print(f"Total artists referenced: {len(all_artists)}")

    # Save artworks
    with open(OUT_FILE, "w") as f:
        json.dump(unique_artworks, f, indent=2, ensure_ascii=False)
    print(f"Saved artworks to {OUT_FILE}")

    # Save artists list separately
    artists_file = os.path.join(os.path.dirname(__file__), "artists.json")
    with open(artists_file, "w") as f:
        json.dump(all_artists, f, indent=2, ensure_ascii=False)
    print(f"Saved artists to {artists_file}")


if __name__ == "__main__":
    main()
