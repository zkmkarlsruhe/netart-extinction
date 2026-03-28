#!/usr/bin/env python3
"""
Scrape net art works from computerfinearts.com via the Wayback Machine.

computerfinearts.com was a pioneering online gallery of digital/net art,
now defunct. Its collection is archived at the Wayback Machine and also
preserved by the Cornell University Library Rose Goldsen Archive.

Structure: /collection/{artist_slug}/{artwork_slug}/
"""

import json
import re
import time
import urllib.request
import urllib.parse
from html import unescape

OUTPUT = "data/sources/computerfinearts/artworks.json"
BASE_DOMAIN = "computerfinearts.com"
CDX_API = "https://web.archive.org/cdx/search/cdx"
WB_PREFIX = "https://web.archive.org/web"
USER_AGENT = "Mozilla/5.0 (compatible; netart-extinction research project)"
DELAY = 2  # seconds between page fetches

# Mapping from directory slug to proper artist name.
# Compiled from the /collection/00__About/ page.
ARTIST_NAMES = {
    "01.org": "0100101110101101.org",
    "abrahams": "Annie Abrahams",
    "ahn": "Sun-Young Ahn",
    "amerika": "Mark Amerika",
    "andrews": "Jim Andrews",
    "arcangel": "Cory Arcangel",
    "biggs": "Simon Biggs",
    "bookchin": "Natalie Bookchin",
    "boredomresearch": "boredomresearch",
    "bravo": "Manik Bravo",
    "breeze": "Mez Breeze",
    "brucker_cohen": "Jonah Brucker-Cohen",
    "bunting": "Heath Bunting",
    "burton": "Ed Burton",
    "cahen": "Xavier Cahen",
    "campbell": "Alexa Campbell",
    "chatonsky": "Gregory Chatonsky",
    "cheang": "Shu Lea Cheang",
    "clauss": "Nicolas Clauss",
    "cloninger": "Curt Cloninger",
    "coyarzun": "Coyarzun",
    "daggett": "Matt Daggett",
    "deck": "Andy Deck",
    "decologne": "Andreas De Cologne",
    "dekok": "Eelco De Kok",
    "doctorhugo": "Doctor Hugo",
    "drouhin": "Reynald Drouhin",
    "easylife.org": "easylife.org",
    "galloway": "Alex Galloway",
    "garrett": "Marc Garrett",
    "geuzen": "Geuzen",
    "grancher": "Valery Grancher",
    "horvath": "Peter Horvath",
    "hourany": "Sami Hourany",
    "hovagimyan": "G.H. Hovagimyan",
    "jevbratt": "Lisa Jevbratt",
    "jimpunk": "jimpunk",
    "KRN": "KRN",
    "kanarek": "Yael Kanarek",
    "klima": "John Klima",
    "lacook": "Lance Lacook",
    "lacook%20-coming": None,  # duplicate
    "lafia": "Mark Lafia",
    "lai": "Tamara Lai",
    "laporta": "Tina LaPorta",
    "lattanzi": "Bill Lattanzi",
    "leckey": "Leckey",
    "leegte": "Jan Robert Leegte",
    "levin": "Golan Levin",
    "lia": "Lia",
    "lialina": "Olia Lialina",
    "lichty": "Patrick Lichty",
    "lo_y": "lo_y",
    "lokiss": "Lokiss",
    "loseby": "Jane Loseby",
    "luining": "Peter Luining",
    "mcdonald": "Jess McDonald",
    "mcelroy": "J&D McElroy",
    "mendoza": "Arcangel Mendoza",
    "mig": "Mig",
    "mouchette": "Mouchette",
    "MTAA": "MTAA",
    "nakamura": "Masato Nakamura",
    "napier": "Mark Napier",
    "navas": "Eduardo Navas",
    "nechvatal": "Joseph Nechvatal",
    "nelson": "Jason Nelson",
    "packer": "Randall Packer",
    "pavu": "pavu.com",
    "peppermint": "Cary Peppermint",
    "polli": "Andrea Polli",
    "rackham": "Melinda Rackham",
    "RSG": "RSG (Radical Software Group)",
    "schmitt": "Axel Schmitt",
    "shulgin": "Alexei Shulgin",
    "simon": "John F. Simon Jr.",
    "sodeoka": "Yoshi Sodeoka",
    "sondheim": "Alan Sondheim",
    "stanza": "Stanza",
    "stern": "Nathaniel Stern",
    "stromajer": "Igor Stromajer",
    "szpakowski": "Michal Szpakowski",
    "takeo": "Michael Takeo Magruder",
    "thomson_craighead": "Thomson & Craighead",
    "todd": "Brian Todd",
    "tribe": "Mark Tribe",
    "utensil": "Utensil",
    "van_anden": "Jim Van Anden",
    "walczak": "Marek Walczak",
    "wattenberg": "Martin Wattenberg",
    "weintraub": "Annette Weintraub",
    "wood": "Paul Wood",
    "YOUNG_HAE_CHANG_HEAVY_INDUSTRIES": "Young-Hae Chang Heavy Industries",
    "zanni": "Carlo Zanni",
    "zden": "Zden",
    "zeleznikar": "Jaka Zeleznikar",
    "zellen": "Jody Zellen",
    "zhang": "Zhang Ga",
    "zurkow": "Marina Zurkow",
    "kalogera%20-coming": None,  # not yet added
}


def fetch(url, timeout=30):
    """Fetch a URL with polite delay and user agent."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def get_collection_structure():
    """Use CDX API to discover artist/artwork directory pairs."""
    url = (
        f"{CDX_API}?url={BASE_DOMAIN}/collection/*"
        f"&output=json&limit=5000"
        f"&fl=timestamp,original,statuscode"
        f"&filter=statuscode:200"
        f"&collapse=urlkey"
    )
    data = fetch(url)
    if not data:
        return {}, {}

    rows = json.loads(data)

    # Extract artist dirs and artist/artwork pairs
    artist_timestamps = {}  # artist_slug -> latest timestamp
    artworks = {}  # (artist_slug, artwork_slug) -> latest timestamp

    for row in rows[1:]:  # skip header
        ts, orig, status = row
        path = urllib.parse.urlparse(orig).path

        # Artist directory: /collection/{artist}/
        m = re.match(r"^/collection/([^/]+)/$", path)
        if m:
            slug = m.group(1)
            if slug not in ("00__About", "About"):
                if slug not in artist_timestamps or ts > artist_timestamps[slug]:
                    artist_timestamps[slug] = ts

        # Artwork directory: /collection/{artist}/{artwork}/
        m = re.match(r"^/collection/([^/]+)/([^/]+)/$", path)
        if m:
            artist = m.group(1)
            work = m.group(2)
            if artist not in ("00__About", "About"):
                key = (artist, work)
                if key not in artworks or ts > artworks[key]:
                    artworks[key] = ts

    return artist_timestamps, artworks


def fetch_artwork_title(artist_slug, artwork_slug, timestamp):
    """Fetch the artwork's index page and extract the <title>."""
    # Try the artwork directory index
    orig_url = f"http://www.computerfinearts.com/collection/{artist_slug}/{artwork_slug}/"
    wb_url = f"{WB_PREFIX}/{timestamp}/{orig_url}"

    html = fetch(wb_url)
    if not html:
        return None

    # Extract <title>
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if m:
        title = m.group(1).strip()
        title = unescape(title)
        title = re.sub(r"\s+", " ", title)
        # Filter out generic/useless titles
        skip = [
            "index of", "404", "untitled document", "apache",
            "not found", "403 forbidden", "wayback machine",
        ]
        if any(s in title.lower() for s in skip):
            return None
        if len(title) > 200:
            return None
        if title.lower() == "index":
            return None
        # Clean up titles with redundant site/artist info
        cleanups = [
            (r" - pavu\.com at computerfinearts\.com$", ""),
            (r"^Web Biennial \d+ - .+ - ", ""),
            (r"^web biennial \d+ -- .+ -- ", ""),
            (r" / Thomson & Craighead$", ""),
            (r"Thomson&Craighead;", "Thomson & Craighead"),
            (r"^Michael Takeo Magruder : \| (.+) \|$", r"\1"),
            (r" - Joseph Nechvatal & Music2eye$", ""),
            (r", by napier$", ""),
            (r"^explore: ", ""),
            (r"^cary peppermint says: ", ""),
        ]
        for pat, repl in cleanups:
            title = re.sub(pat, repl, title)
        return title

    return None


def slug_to_title(slug):
    """Convert an artwork directory slug to a readable title."""
    # Clean up common patterns
    title = slug.replace("_", " ").replace("-", " ")
    # Title-case if all lowercase
    if title == title.lower():
        title = title.title()
    return title


def main():
    print("Fetching collection structure from CDX API...")
    artist_timestamps, artworks = get_collection_structure()
    print(f"Found {len(artist_timestamps)} artists, {len(artworks)} artwork directories")

    if not artworks:
        print("No artworks found! Exiting.")
        return

    results = []
    seen = set()

    # For each artwork, try to fetch the title from the page
    sorted_artworks = sorted(artworks.items(), key=lambda x: (x[0][0], x[0][1]))

    for i, ((artist_slug, artwork_slug), timestamp) in enumerate(sorted_artworks):
        # Skip duplicates (e.g. lacook%20-coming is same as lacook)
        artist_name = ARTIST_NAMES.get(artist_slug)
        if artist_name is None:
            # Check URL-decoded version
            decoded = urllib.parse.unquote(artist_slug)
            artist_name = ARTIST_NAMES.get(decoded)
            if artist_name is None:
                artist_name = decoded.replace("_", " ").title()

        dedup_key = (artist_name.lower(), artwork_slug.lower())
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        orig_url = f"http://www.computerfinearts.com/collection/{artist_slug}/{artwork_slug}/"
        wayback_url = f"{WB_PREFIX}/{timestamp}/{orig_url}"

        print(f"  [{i+1}/{len(sorted_artworks)}] {artist_slug}/{artwork_slug} ...", end=" ", flush=True)

        # Fetch the page to get the title
        title = fetch_artwork_title(artist_slug, artwork_slug, timestamp)
        time.sleep(DELAY)

        if title:
            print(f"-> {title}")
        else:
            title = slug_to_title(artwork_slug)
            print(f"-> (from slug) {title}")

        results.append({
            "source": "computerfinearts",
            "source_url": wayback_url,
            "title": title,
            "artist": artist_name,
            "year": None,
            "url": orig_url,
            "medium": "Net art",
        })

    # Also add artists that have a directory but no artwork subdirectories
    # (their work might be directly in the artist dir)
    artists_with_works = {a for a, _ in artworks.keys()}
    for artist_slug, ts in sorted(artist_timestamps.items()):
        if artist_slug not in artists_with_works:
            artist_name = ARTIST_NAMES.get(artist_slug)
            if artist_name is None:
                decoded = urllib.parse.unquote(artist_slug)
                artist_name = ARTIST_NAMES.get(decoded)
                if artist_name is None:
                    artist_name = decoded.replace("_", " ").title()

            # Try to fetch their page for a title
            orig_url = f"http://www.computerfinearts.com/collection/{artist_slug}/"
            wb_url = f"{WB_PREFIX}/{ts}/{orig_url}"

            print(f"  Artist-only: {artist_slug} ...", end=" ", flush=True)
            html = fetch(wb_url)
            time.sleep(DELAY)

            if html:
                # Look for links to HTML files in the directory
                page_links = re.findall(
                    r'href=["\']([^"\']+\.html?)["\']', html, re.I
                )
                page_links = [
                    l for l in page_links
                    if "archive.org" not in l and "?" not in l
                ]
                if page_links:
                    # This artist has HTML files directly in their dir
                    # Treat the artist dir as a single work
                    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
                    title = None
                    if m:
                        t = unescape(m.group(1).strip())
                        t = re.sub(r"\s+", " ", t)
                        skip = ["index of", "404", "untitled", "apache", "not found"]
                        if not any(s in t.lower() for s in skip):
                            title = t

                    if not title:
                        title = f"{artist_name} (collection page)"
                        # Skip generic collection pages
                        print(f"-> skipped (directory listing)")
                        continue

                    print(f"-> {title}")
                    results.append({
                        "source": "computerfinearts",
                        "source_url": wb_url,
                        "title": title,
                        "artist": artist_name,
                        "year": None,
                        "url": orig_url.replace(":80", ""),
                        "medium": "Net art",
                    })
                else:
                    print(f"-> skipped (no content)")
            else:
                print(f"-> skipped (fetch failed)")

    # Clean up URLs - remove :80 port
    for r in results:
        r["url"] = r["url"].replace(":80", "")

    # Sort by artist, then title
    results.sort(key=lambda x: (x["artist"].lower(), x["title"].lower()))

    print(f"\nTotal artworks: {len(results)}")
    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    main()
