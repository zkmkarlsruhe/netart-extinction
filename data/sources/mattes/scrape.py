#!/usr/bin/env python3
"""Scrape artworks from Eva and Franco Mattes' website."""

import json
import re
import urllib.request

URL = "https://0100101110101101.org/works/"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode("utf-8")

# Extract the entry-content div
content_match = re.search(r'<div class="entry-content">(.*?)</div>', html, re.DOTALL)
if not content_match:
    raise RuntimeError("Could not find entry-content div")

content = content_match.group(1)

# Each artwork is: <a href="URL">Title</a> (YEAR)
# Year can be like: 2001, 2000-03, 2022-, 2016-21, 2007-10
pattern = r'<a href="([^"]+)">([^<]+)</a>\s*\((\d{4}[^)]*)\)'

artworks = []
for match in re.finditer(pattern, content):
    url, title, year_str = match.groups()

    # Decode HTML entities in title
    title = title.replace("&#8217;", "\u2019")
    title = title.replace("&#8211;", "\u2013")
    title = title.replace("&amp;", "&")
    title = title.replace("&#8216;", "\u2018")
    title = title.replace("&lt;", "<")
    title = title.replace("&gt;", ">")

    # Extract the start year as integer
    year = int(re.match(r"(\d{4})", year_str).group(1))

    artworks.append({
        "source": "0100101110101101.org",
        "source_url": URL,
        "title": title,
        "artist": "Eva and Franco Mattes",
        "year": year,
        "url": url,
        "medium": "Net art",
    })

output_path = "/x/coding/netart-extinction/data/sources/mattes/artworks.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(artworks, f, indent=2, ensure_ascii=False)

print(f"Saved {len(artworks)} artworks to {output_path}")
