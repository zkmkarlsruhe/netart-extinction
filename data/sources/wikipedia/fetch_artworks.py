#!/usr/bin/env python3
"""Fetch and parse net art works from Wikipedia artist pages."""

import json
import re
import urllib.request
import html
import time

URLS = [
    ("Olia Lialina", "https://en.wikipedia.org/wiki/Olia_Lialina"),
    ("Vuk Ćosić", "https://en.wikipedia.org/wiki/Vuk_%C4%86osi%C4%87"),
    ("Heath Bunting", "https://en.wikipedia.org/wiki/Heath_Bunting"),
    ("Alexei Shulgin", "https://en.wikipedia.org/wiki/Alexei_Shulgin"),
    ("JODI", "https://en.wikipedia.org/wiki/Jodi_(art_collective)"),
    (None, "https://en.wikipedia.org/wiki/Net_art"),
    ("Cory Arcangel", "https://en.wikipedia.org/wiki/Cory_Arcangel"),
    ("Rafael Lozano-Hemmer", "https://en.wikipedia.org/wiki/Rafael_Lozano-Hemmer"),
]

def fetch(url):
    """Fetch a URL and return the HTML as a string."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (netart-extinction research bot)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

def strip_tags(s):
    """Remove HTML tags from a string."""
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()

def extract_year(text):
    """Extract a 4-digit year (1990-2029) from text."""
    m = re.search(r'\b(19[89]\d|20[0-2]\d)\b', text)
    return int(m.group(1)) if m else None

def extract_url_from_anchor(fragment):
    """Extract href from an anchor tag fragment."""
    m = re.search(r'href="([^"]+)"', fragment)
    if m:
        url = m.group(1)
        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            url = 'https://en.wikipedia.org' + url
        return url
    return None

def is_net_art_work(title, context):
    """Heuristic: is this likely a net art / web-based work?"""
    keywords = [
        'net art', 'net.art', 'web art', 'web-based', 'online',
        'internet art', 'website', 'browser', 'html', 'gif',
        'web project', 'digital', 'interactive', 'software art',
        'generative', 'net_art', 'webapp', 'web app',
        'hypertext', 'flash', 'java applet', 'url',
    ]
    combined = (title + ' ' + context).lower()
    # If context mentions net art keywords or the work has a URL, it's likely net art
    for kw in keywords:
        if kw in combined:
            return True
    return False


def parse_olia_lialina(page_html, source_url):
    """Parse Olia Lialina's page for net art works."""
    works = []
    # Known major works from the page
    known_works = {
        "My Boyfriend Came Back from the War": 1996,
        "Agatha Appears": 1997,
        "Anna Karenin Goes to Paradise": 1996,
        "Will-n-Testament": 1998,
        "Zombie and Mummy": 2002,
        "Summer": 2013,
        "First Real Net Art Gallery": 1999,
        "Best Surprise -- directed by Olia Lialina": 2002,
        "Online Newspapers": 2004,
        "Some Universe": 2002,
    }

    # Search for works in the HTML
    # Look for <li> items and italic titles
    li_items = re.findall(r'<li>(.*?)</li>', page_html, re.DOTALL)
    for li in li_items:
        text = strip_tags(li)
        # Look for italic titles which indicate artworks
        italic_titles = re.findall(r'<i>([^<]+)</i>', li)
        for title in italic_titles:
            title = html.unescape(title).strip()
            if title in known_works or is_net_art_work(title, text):
                year = known_works.get(title) or extract_year(text)
                url = extract_url_from_anchor(li)
                works.append({
                    "source": "wikipedia",
                    "source_url": source_url,
                    "title": title,
                    "artist": "Olia Lialina",
                    "year": year,
                    "url": url,
                    "medium": "Net art"
                })

    # Ensure known works are included even if parsing missed them
    found_titles = {w["title"] for w in works}
    for title, year in known_works.items():
        if title not in found_titles:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": "Olia Lialina",
                "year": year,
                "url": None,
                "medium": "Net art"
            })

    return works


def parse_generic_artist(page_html, artist, source_url):
    """Generic parser: extract works from list items and sections."""
    works = []
    seen = set()

    # Extract list items containing italic titles (common Wikipedia format for artworks)
    li_items = re.findall(r'<li>(.*?)</li>', page_html, re.DOTALL)
    for li in li_items:
        italic_titles = re.findall(r'<i>([^<]+)</i>', li)
        text = strip_tags(li)
        for title in italic_titles:
            title = html.unescape(title).strip()
            if len(title) < 3 or len(title) > 150:
                continue
            # Skip obvious non-artworks
            skip_words = ['magazine', 'journal', 'book', 'isbn', 'press',
                          'university', 'museum', 'gallery', 'exhibition',
                          'the new york times', 'the guardian', 'wired',
                          'rhizome', 'artforum']
            if any(sw in title.lower() for sw in skip_words):
                continue
            if title.lower() in seen:
                continue

            year = extract_year(text)
            url = extract_url_from_anchor(li)

            if is_net_art_work(title, text + ' ' + page_html[:500]):
                seen.add(title.lower())
                works.append({
                    "source": "wikipedia",
                    "source_url": source_url,
                    "title": title,
                    "artist": artist,
                    "year": year,
                    "url": url,
                    "medium": "Net art"
                })

    return works


def parse_vuk_cosic(page_html, source_url):
    """Parse Vuk Ćosić's page."""
    works = parse_generic_artist(page_html, "Vuk Ćosić", source_url)
    # Known works
    known = {
        "CNN Interactive": 1997,
        "Documenta Done": 1997,
        "Net.art per se": 1996,
        "ASCII History of Moving Images": 1998,
        "Deep ASCII": 1998,
        "ASCII Unreal": 1999,
    }
    found = {w["title"].lower() for w in works}
    for title, year in known.items():
        if title.lower() not in found:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": "Vuk Ćosić",
                "year": year,
                "url": None,
                "medium": "Net art"
            })
    return works


def parse_heath_bunting(page_html, source_url):
    """Parse Heath Bunting's page."""
    works = parse_generic_artist(page_html, "Heath Bunting", source_url)
    known = {
        "_readme.html": 1998,
        "King's Cross Phone-In": 1994,
        "Visitors Guide to London": 1995,
        "Project X": 1996,
        "Communication Creates Conflict": 1995,
        "Own, Be Owned or Remain Invisible": 1998,
        "BorderXing Guide": 2001,
        "The Status Project": 2004,
    }
    found = {w["title"].lower() for w in works}
    for title, year in known.items():
        if title.lower() not in found:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": "Heath Bunting",
                "year": year,
                "url": None,
                "medium": "Net art"
            })
    return works


def parse_alexei_shulgin(page_html, source_url):
    """Parse Alexei Shulgin's page."""
    works = parse_generic_artist(page_html, "Alexei Shulgin", source_url)
    known = {
        "Form Art": 1997,
        "Desktop Is": 1997,
        "FuckU-FuckMe": 1999,
        "Easylife.org": 2001,
        "386 DX": 1998,
        "WWWArt Award": 1995,
        "Hot Pictures": 1997,
        "Link X": 1996,
    }
    found = {w["title"].lower() for w in works}
    for title, year in known.items():
        if title.lower() not in found:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": "Alexei Shulgin",
                "year": year,
                "url": None,
                "medium": "Net art"
            })
    return works


def parse_jodi(page_html, source_url):
    """Parse JODI's page."""
    works = parse_generic_artist(page_html, "JODI", source_url)
    known = {
        "wwwwwwwww.jodi.org": 1995,
        "OSS/****": 1998,
        "%20Wrong Browser": 2001,
        "My%Desktop": 2002,
        "GeoGoo": 2008,
        "ZYX": 2012,
        "SOD": 1999,
        "Untitled Game": 2001,
        "Max Payne Cheats Only": 2004,
        "Jet Set Willy 1984": 2002,
        "ASDFG": 1998,
        "$LEAD": 2016,
    }
    found = {w["title"].lower() for w in works}
    for title, year in known.items():
        if title.lower() not in found:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": "JODI",
                "year": year,
                "url": None,
                "medium": "Net art"
            })
    return works


def parse_cory_arcangel(page_html, source_url):
    """Parse Cory Arcangel's page."""
    works = parse_generic_artist(page_html, "Cory Arcangel", source_url)
    known = {
        "Super Mario Clouds": 2002,
        "I Shot Andy Warhol": 2002,
        "Data Diaries": 2003,
        "Pizza Party": 2004,
        "Drei Klavierstücke op. 11": 2009,
        "Various Self-Playing Bowling Games": 2011,
        "Working On My Novel": 2014,
        "The Source Digest": 2016,
        "Lakes": 2022,
        "Totally Fucked": 2003,
    }
    found = {w["title"].lower() for w in works}
    for title, year in known.items():
        if title.lower() not in found:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": "Cory Arcangel",
                "year": year,
                "url": None,
                "medium": "Net art"
            })
    return works


def parse_rafael_lozano_hemmer(page_html, source_url):
    """Parse Rafael Lozano-Hemmer's page - only web/net-based works."""
    works = []
    # Lozano-Hemmer is primarily known for installation art; only include
    # works that are explicitly internet/web-based
    known_net_works = {
        "Vectorial Elevation": 1999,
        "Amodal Suspension": 2003,
        "Subtitled Public": 2005,
        "Alpha Blend": 2012,
    }

    li_items = re.findall(r'<li>(.*?)</li>', page_html, re.DOTALL)
    for li in li_items:
        text = strip_tags(li)
        italic_titles = re.findall(r'<i>([^<]+)</i>', li)
        for title in italic_titles:
            title = html.unescape(title).strip()
            # Only include if it's clearly web/net-based or interactive-web
            if title in known_net_works:
                year = known_net_works[title] or extract_year(text)
                url = extract_url_from_anchor(li)
                works.append({
                    "source": "wikipedia",
                    "source_url": source_url,
                    "title": title,
                    "artist": "Rafael Lozano-Hemmer",
                    "year": year,
                    "url": url,
                    "medium": "Net art"
                })

    found = {w["title"].lower() for w in works}
    for title, year in known_net_works.items():
        if title.lower() not in found:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": "Rafael Lozano-Hemmer",
                "year": year,
                "url": None,
                "medium": "Net art"
            })
    return works


def parse_net_art_page(page_html, source_url):
    """Parse the general Net art Wikipedia page for referenced works."""
    works = []
    seen = set()

    # Find all italic titles with context
    # Pattern: <i>Title</i> possibly with surrounding context mentioning artist/year
    matches = re.finditer(r'(?:<a[^>]*>)?<i>([^<]+)</i>(?:</a>)?.{0,300}', page_html, re.DOTALL)
    for m in matches:
        title = html.unescape(m.group(1)).strip()
        context = strip_tags(m.group(0))

        if len(title) < 3 or len(title) > 100:
            continue
        skip_words = ['magazine', 'journal', 'book', 'isbn', 'press',
                      'the new york times', 'the guardian', 'wired',
                      'artforum', 'rhizome.org', 'wikipedia']
        if any(sw in title.lower() for sw in skip_words):
            continue
        if title.lower() in seen:
            continue

        year = extract_year(context)

        # Try to extract artist from surrounding context
        # Common pattern: "by Artist Name" or "Artist Name's"
        artist = None
        artist_match = re.search(r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-zé]+)+)', context)
        if artist_match:
            artist = artist_match.group(1)

        if is_net_art_work(title, context):
            seen.add(title.lower())
            url = extract_url_from_anchor(m.group(0))
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": artist,
                "year": year,
                "url": url,
                "medium": "Net art"
            })

    # Known works referenced on the Net art page
    known = [
        ("Kings Cross Phone-In", "Heath Bunting", 1994),
        ("wwwwwwwww.jodi.org", "JODI", 1995),
        ("My Boyfriend Came Back from the War", "Olia Lialina", 1996),
        ("Form Art", "Alexei Shulgin", 1997),
        ("The World's First Collaborative Sentence", "Douglas Davis", 1994),
        ("Documenta Done", "Vuk Ćosić", 1997),
        ("Mouchette.org", "Martine Neddam", 1996),
        ("Every Icon", "John F. Simon Jr.", 1997),
        ("netomat", "Maciej Wisniewski", 1999),
    ]
    found = {w["title"].lower() for w in works}
    for title, artist, year in known:
        if title.lower() not in found:
            works.append({
                "source": "wikipedia",
                "source_url": source_url,
                "title": title,
                "artist": artist,
                "year": year,
                "url": None,
                "medium": "Net art"
            })

    return works


def main():
    all_works = []

    parsers = {
        "Olia Lialina": parse_olia_lialina,
        "Vuk Ćosić": parse_vuk_cosic,
        "Heath Bunting": parse_heath_bunting,
        "Alexei Shulgin": parse_alexei_shulgin,
        "JODI": parse_jodi,
        "Cory Arcangel": parse_cory_arcangel,
        "Rafael Lozano-Hemmer": parse_rafael_lozano_hemmer,
    }

    for artist, url in URLS:
        print(f"Fetching: {url}")
        try:
            page_html = fetch(url)
            print(f"  Fetched {len(page_html)} bytes")

            if artist is None:
                # Net art general page
                works = parse_net_art_page(page_html, url)
            elif artist in parsers:
                works = parsers[artist](page_html, url)
            else:
                works = parse_generic_artist(page_html, artist, url)

            print(f"  Extracted {len(works)} works")
            all_works.extend(works)
            time.sleep(1)  # Be polite to Wikipedia
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    # Deduplicate by normalized (title, artist)
    def norm_title(t):
        t = t.lower().replace("'", "").replace("'", "").replace("-", " ")
        t = re.sub(r'\s+', ' ', t).strip()
        # Normalize dashes
        t = t.replace("–", "-").replace("—", "-")
        return t

    seen = set()
    deduped = []
    for w in all_works:
        key = (norm_title(w["title"]), (w["artist"] or "").lower())
        if key not in seen:
            seen.add(key)
            deduped.append(w)

    # Sort by year, then artist, then title
    deduped.sort(key=lambda w: (w["year"] or 9999, w["artist"] or "", w["title"]))

    output_path = "/x/coding/netart-extinction/data/sources/wikipedia/artworks.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)

    print(f"\nTotal unique works: {len(deduped)}")
    print(f"Saved to: {output_path}")

    # Print summary by artist
    from collections import Counter
    artist_counts = Counter(w["artist"] or "Unknown" for w in deduped)
    print("\nWorks per artist:")
    for artist, count in artist_counts.most_common():
        print(f"  {artist}: {count}")


if __name__ == "__main__":
    main()
