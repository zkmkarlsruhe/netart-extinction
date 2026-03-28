#!/usr/bin/env python3
"""
Scrape Rhizome Net Art Anthology artworks from sites.rhizome.org/anthology/
and save as normalized JSON.
"""

import json
import re
import urllib.request
import html as html_module

URL = "https://sites.rhizome.org/anthology/"

def fetch_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")

def parse_year(year_str):
    """Extract a single integer year (the start year) from strings like '1996', '1996-1999', 'c. 2000-2008', '2008 - 2011'."""
    year_str = year_str.strip()
    # Remove circa prefix
    year_str = re.sub(r'^c\.\s*', '', year_str)
    # Find the first 4-digit year
    m = re.search(r'(\d{4})', year_str)
    if m:
        return int(m.group(1))
    return None

def parse_artworks(html_text):
    # Each <li> contains a link and a Go template map with metadata
    # Pattern: <a href="...">Title</a> map[artist:... title:... year:...]
    li_pattern = re.compile(
        r'<li><a href="([^"]+)">([^<]+)</a>\s*map\[(.+?)\]</li>',
        re.DOTALL
    )

    # Parse key:value pairs from Go map string
    # Keys are: artist, browser, color, custom, embed, height, title, width, year
    # Values can contain spaces, so we match key:value where key is a known word
    known_keys = ['artist', 'browser', 'color', 'custom', 'embed', 'height', 'title', 'width', 'year']

    def parse_map(map_str):
        """Parse Go-style map[k1:v1 k2:v2 ...] into a dict."""
        result = {}
        # Build pattern that splits on known keys
        # We find all key:value pairs where key is a known key
        key_pattern = '|'.join(known_keys)
        parts = re.split(r'\s+(?=(?:' + key_pattern + r'):)', map_str)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            colon_idx = part.find(':')
            if colon_idx == -1:
                continue
            key = part[:colon_idx]
            value = part[colon_idx+1:]
            if key in known_keys:
                result[key] = value
        return result

    seen = {}  # title+artist -> entry, to deduplicate solo/live variants
    artworks = []

    for match in li_pattern.finditer(html_text):
        href = match.group(1)
        link_title = html_module.unescape(match.group(2).strip())
        map_str = match.group(3)

        meta = parse_map(map_str)

        title = html_module.unescape(meta.get('title', link_title))
        artist = html_module.unescape(meta.get('artist', ''))
        year_raw = meta.get('year', '')
        year = parse_year(year_raw)

        # Build the canonical anthology URL
        if href.startswith('/'):
            artwork_url = "https://sites.rhizome.org" + href
        else:
            artwork_url = URL + href

        # Deduplicate: skip "-solo" and variant pages for same work
        dedup_key = (title, artist)
        if dedup_key in seen:
            # Keep the shorter/cleaner URL (non-solo version)
            if '-solo' in href or '-live' in href:
                continue
            # If existing one is solo/live, replace it
            existing_href = seen[dedup_key]['_href']
            if '-solo' in existing_href or '-live' in existing_href:
                # Replace the existing entry
                for i, a in enumerate(artworks):
                    if a['title'] == title and a['artist'] == artist:
                        artworks[i]['url'] = artwork_url
                        seen[dedup_key]['_href'] = href
                        break
                continue
            # Both are non-solo variants (e.g. Form Art vs Form Art Competition) - keep both
            # Actually check if titles differ
            if title == seen[dedup_key]['_title']:
                continue

        entry = {
            "source": "rhizome-anthology",
            "source_url": URL,
            "title": title,
            "artist": artist,
            "year": year,
            "year_display": year_raw if year_raw != str(year) else None,
            "url": artwork_url,
            "medium": "Net art",
            "_href": href,
            "_title": title,
        }
        seen[dedup_key] = entry
        artworks.append(entry)

    # Clean up internal fields and None year_display
    for a in artworks:
        del a['_href']
        del a['_title']
        if a['year_display'] is None:
            del a['year_display']

    return artworks

def main():
    print(f"Fetching {URL} ...")
    html_text = fetch_page(URL)
    print(f"Fetched {len(html_text)} bytes")

    artworks = parse_artworks(html_text)
    print(f"Parsed {len(artworks)} unique artworks")

    # Sort by year, then title
    artworks.sort(key=lambda a: (a['year'] or 9999, a['title']))

    output_path = "/x/coding/netart-extinction/data/sources/rhizome-anthology/artworks.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(artworks, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_path}")

    # Print summary
    for a in artworks:
        print(f"  {a['year']}  {a['title']} — {a['artist']}")

if __name__ == "__main__":
    main()
