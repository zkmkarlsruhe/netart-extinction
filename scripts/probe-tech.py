#!/usr/bin/env python3
"""
Probe artwork URLs to detect technology dependencies.

Checks HTTP headers and HTML content for tech signatures:
- Flash: .swf embeds, x-shockwave-flash content type
- Java: applet tags, .jar/.class references
- QuickTime: .mov embeds, quicktime plugin
- Shockwave: .dcr embeds, x-director content type
- VRML: .wrl links, x-vrml content type
- RealPlayer: .rm/.ram embeds
- Silverlight: .xap embeds
- ActiveX: classid/codebase params
- MIDI: .mid embeds
- etc.

Uses Wayback Machine CDX API first to check if page is archived,
then probes the archived version for tech signatures.
"""

import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = Path(__file__).parent.parent
ARTWORKS_DIR = PROJECT_ROOT / "src" / "content" / "artworks"
CACHE_FILE = PROJECT_ROOT / "scripts" / "output" / "tech-probe-cache.json"

# HTML signatures for technology detection
HTML_SIGNATURES = [
    (r'\.swf["\'\s?]', 'Flash'),
    (r'application/x-shockwave-flash', 'Flash'),
    (r'<embed[^>]*flash', 'Flash'),
    (r'swfobject', 'Flash'),
    (r'<applet\b', 'Java Applet'),
    (r'\.jar["\'\s?]', 'Java Applet'),
    (r'\.class["\'\s?]', 'Java Applet'),
    (r'application/x-java', 'Java Applet'),
    (r'\.dcr["\'\s?]', 'Shockwave'),
    (r'application/x-director', 'Shockwave'),
    (r'\.dir["\'\s?]', 'Macromedia Director'),
    (r'<embed[^>]*quicktime', 'QuickTime'),
    (r'\.mov["\'\s?]', 'QuickTime'),
    (r'video/quicktime', 'QuickTime'),
    (r'\.wrl["\'\s?]', 'VRML'),
    (r'model/vrml', 'VRML'),
    (r'x-vrml', 'VRML'),
    (r'cosmo\s*player', 'VRML'),
    (r'\.xap["\'\s?]', 'Silverlight'),
    (r'application/x-silverlight', 'Silverlight'),
    (r'silverlight\.js', 'Silverlight'),
    (r'classid\s*=\s*["\']clsid:', 'ActiveX'),
    (r'\.mid["\'\s?]', 'MIDI'),
    (r'audio/midi', 'MIDI'),
    (r'bgsound', 'MIDI'),
    (r'\.rm["\'\s?]', 'RealPlayer'),
    (r'\.ram["\'\s?]', 'RealAudio'),
    (r'audio/x-pn-realaudio', 'RealAudio'),
    (r'<iframe\b', 'iframe'),
    (r'\.php["\'\s?]', 'PHP'),
    (r'\.asp["\'\s?]', 'ASP'),
    (r'\.cgi["\'\s?]', 'CGI'),
    (r'\.pl["\'\s?]', 'Perl'),
    (r'webgl', 'WebGL'),
    (r'three\.js', 'WebGL'),
    (r'p5\.js', 'p5.js'),
    (r'processing\.js', 'Processing'),
    (r'jquery', 'JavaScript'),
]

COMPILED_SIGS = [(re.compile(p, re.I), tech) for p, tech in HTML_SIGNATURES]


def fetch_url(url, timeout=10):
    """Fetch URL content, return (html, content_type) or (None, None)."""
    try:
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (research project; +https://github.com/zkmkarlsruhe/netart-extinction)',
        })
        resp = urlopen(req, timeout=timeout)
        ct = resp.headers.get('Content-Type', '')
        if 'text/html' in ct or 'text/plain' in ct:
            html = resp.read(100_000).decode('utf-8', errors='replace')
            return html, ct
        return None, ct
    except Exception:
        return None, None


def detect_tech_from_html(html):
    """Detect technologies from HTML content."""
    techs = set()
    for pattern, tech in COMPILED_SIGS:
        if pattern.search(html):
            techs.add(tech)
    return techs


def wayback_url(url):
    """Get the most recent Wayback Machine capture URL."""
    api = f"https://archive.org/wayback/available?url={url}"
    try:
        req = Request(api, headers={'User-Agent': 'netart-extinction-research/1.0'})
        resp = urlopen(req, timeout=10)
        data = json.loads(resp.read())
        snapshot = data.get('archived_snapshots', {}).get('closest', {})
        if snapshot.get('available'):
            return snapshot['url']
    except Exception:
        pass
    return None


def probe_artwork(url, use_wayback=True):
    """Probe a URL for technology signatures. Returns set of tech names."""
    techs = set()

    # Try live URL first
    html, ct = fetch_url(url)
    if html:
        techs.update(detect_tech_from_html(html))
    elif ct:
        # Non-HTML content type might tell us something
        if 'shockwave' in (ct or '').lower():
            techs.add('Flash')
        if 'director' in (ct or '').lower():
            techs.add('Shockwave')

    # If nothing found and URL is dead, try Wayback
    if not techs and use_wayback and html is None:
        wb_url = wayback_url(url)
        if wb_url:
            html, ct = fetch_url(wb_url)
            if html:
                techs.update(detect_tech_from_html(html))

    # Filter out overly generic detections
    techs.discard('iframe')  # too common
    techs.discard('JavaScript')  # too common

    return techs


def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}


def save_cache(cache):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2))


def main():
    cache = load_cache()

    # Collect all artworks needing probing
    to_probe = []
    for f in sorted(os.listdir(ARTWORKS_DIR)):
        if not f.endswith('.md'):
            continue
        text = open(ARTWORKS_DIR / f).read()
        if 'technologies:' in text:
            continue  # already tagged
        url_m = re.search(r'url:\s*"(https?://[^"]+)"', text)
        if not url_m:
            continue
        url = url_m.group(1)
        # Skip known-dead patterns
        if 'ntticc.or.jp' in url:
            continue  # catalog pages, not the actual work
        to_probe.append((f, url))

    print(f"Artworks to probe: {len(to_probe)}")

    # Filter out cached
    uncached = [(f, url) for f, url in to_probe if url not in cache]
    print(f"Uncached: {len(uncached)}")
    print(f"Cached: {len(to_probe) - len(uncached)}")

    # Probe uncached URLs (with rate limiting)
    for i, (f, url) in enumerate(uncached):
        if i > 0 and i % 10 == 0:
            print(f"  Probed {i}/{len(uncached)}...")
            save_cache(cache)

        techs = probe_artwork(url, use_wayback=True)
        cache[url] = list(techs)
        time.sleep(0.5)  # rate limit

    save_cache(cache)

    # Apply results
    tagged = 0
    for f, url in to_probe:
        techs = cache.get(url, [])
        if not techs:
            continue

        filepath = ARTWORKS_DIR / f
        text = filepath.read_text()
        fm_end = text.index('---', 3)
        fm = text[3:fm_end].strip()
        body = text[fm_end + 3:]

        tech_yaml = "technologies:\n" + "\n".join(f'  - "{t}"' for t in sorted(set(techs)))
        if 'ai_generated:' in fm:
            fm = fm.replace('ai_generated:', f'{tech_yaml}\nai_generated:')
        else:
            fm = fm + "\n" + tech_yaml

        filepath.write_text(f"---\n{fm}\n---{body}")
        tagged += 1

    print(f"\nNewly tagged: {tagged}")
    print(f"Total probed: {len(to_probe)}")


if __name__ == "__main__":
    main()
