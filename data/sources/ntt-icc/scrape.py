#!/usr/bin/env python3
"""Scrape artworks from the NTT ICC (InterCommunication Center) archive."""

import json
import re
import time
import urllib.request
from html.parser import HTMLParser

BASE = "https://www.ntticc.or.jp"
YEAR_URL = BASE + "/en/archive/works/{year}/"
OUTPUT = "/x/coding/03-websites/netart-extinction/data/sources/ntt-icc/artworks.json"
DELAY = 0.5


class ICCParser(HTMLParser):
    """Parse ICC archive year pages to extract artwork entries.

    Actual HTML structure:
        <a href="/en/archive/works/slug/" class="...media_vertical--works">
          <div class="media__content">
            <div class="media_content__header">
              <h3 class="media__content__title ...">
                "Title"
                <span class="media__content__title__date">[date]</span>
              </h3>
            </div>
            <div class="media__content__footer">
              <span class="fs-4">Artist Name</span>
            </div>
          </div>
        </a>
    """

    def __init__(self):
        super().__init__()
        self.artworks = []
        self.in_artwork_link = False
        self.current_href = ""
        self.in_title = False       # inside h3.media__content__title
        self.in_title_date = False   # inside span.media__content__title__date
        self.in_footer = False       # inside div.media__content__footer
        self.in_footer_span = False  # inside span within footer
        self.current_title = ""
        self.current_artist = ""
        self.a_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get("class", "")

        if tag == "a":
            href = attrs_dict.get("href", "")
            if re.match(r"/en/archive/works/[^/]+/$", href):
                self.in_artwork_link = True
                self.current_href = href
                self.current_title = ""
                self.current_artist = ""
                self.a_depth = 0
            if self.in_artwork_link:
                self.a_depth += 1

        elif self.in_artwork_link:
            if tag == "h3" and "media__content__title" in cls:
                self.in_title = True
            elif tag == "span" and "media__content__title__date" in cls:
                self.in_title_date = True
            elif tag == "div" and "media__content__footer" in cls:
                self.in_footer = True
            elif tag == "span" and self.in_footer:
                self.in_footer_span = True

    def handle_endtag(self, tag):
        if tag == "h3":
            self.in_title = False
        elif tag == "span" and self.in_title_date:
            self.in_title_date = False
        elif tag == "div" and self.in_footer:
            self.in_footer = False
        elif tag == "span" and self.in_footer_span:
            self.in_footer_span = False

        if self.in_artwork_link and tag == "a":
            self.a_depth -= 1
            if self.a_depth <= 0:
                self.in_artwork_link = False
                if self.current_title or self.current_artist:
                    self.artworks.append({
                        "href": self.current_href,
                        "title": self.current_title.strip(),
                        "artist": self.current_artist.strip(),
                    })

    def handle_data(self, data):
        if self.in_title and not self.in_title_date:
            self.current_title += data
        elif self.in_footer_span:
            self.current_artist += data


def clean_title(raw_title):
    """Remove surrounding quotes and date brackets from title."""
    # e.g. '"Valence" [2001–]' -> 'Valence'
    # Strip leading/trailing whitespace
    t = raw_title.strip()
    # Remove date portion in brackets at the end: [2001], [2001–], [2001/10/25], etc.
    t = re.sub(r"\s*\[.*?\]\s*$", "", t)
    # Remove surrounding quotes (straight or smart)
    t = re.sub(r'^[\u201c\u201d""\']+|[\u201c\u201d""\']+$', "", t)
    return t.strip()


def fetch_year(year):
    """Fetch and parse a single year page. Returns list of artwork dicts."""
    url = YEAR_URL.format(year=year)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (research bot; net art archive project)",
        "Accept": "text/html",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR fetching {url}: {e}")
        return []

    parser = ICCParser()
    parser.feed(html)

    results = []
    for item in parser.artworks:
        title = clean_title(item["title"])
        if not title:
            continue
        work_url = BASE + item["href"] if item["href"].startswith("/") else item["href"]
        results.append({
            "source": "ntt-icc",
            "source_url": url,
            "title": title,
            "artist": item["artist"],
            "year": year,
            "url": work_url,
            "medium": "Media art",
        })
    return results


def main():
    all_artworks = []
    for year in range(1991, 2026):
        print(f"Fetching {year}...", end=" ", flush=True)
        works = fetch_year(year)
        print(f"{len(works)} works")
        all_artworks.extend(works)
        time.sleep(DELAY)

    # Deduplicate by URL (same work can appear in multiple years)
    seen = set()
    unique = []
    for w in all_artworks:
        if w["url"] not in seen:
            seen.add(w["url"])
            unique.append(w)

    print(f"\nTotal: {len(all_artworks)} entries, {len(unique)} unique works")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    print(f"Saved to {OUTPUT}")


if __name__ == "__main__":
    main()
