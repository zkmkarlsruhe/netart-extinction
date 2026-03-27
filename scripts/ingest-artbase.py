#!/usr/bin/env python3
"""
Ingest artworks from Rhizome ArtBase and match them to extinction events.

Pipeline:
1. SPARQL query ArtBase for all artworks with technology-related tags
2. Extract technology dependencies from legacy tags
3. Match to existing extinction events in src/content/events/
4. For ambiguous cases, use SAIA LLM to classify
5. Output new artwork .md files and update events with affected_artworks
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode

# ── Config ──────────────────────────────────────────────────────────────────

SPARQL_URL = "https://query.artbase.rhizome.org/proxy/wdqs/bigdata/namespace/wdq/sparql"
SAIA_BASE_URL = os.getenv("SAIA_BASE_URL", "https://chat-ai.academiccloud.de/v1")
SAIA_API_KEY = os.getenv("SAIA_API_KEY", "")
SAIA_MODEL = "mistral-large-3-675b-instruct-2512"

PROJECT_ROOT = Path(__file__).parent.parent
ARTWORKS_DIR = PROJECT_ROOT / "src" / "content" / "artworks"
EVENTS_DIR = PROJECT_ROOT / "src" / "content" / "events"
OUTPUT_DIR = PROJECT_ROOT / "scripts" / "output"

# Technology keywords → extinction event slug mapping
TECH_TO_EVENT = {
    "flash": "flash-player-blocked",
    "shockwave": "shockwave-player-eol",
    "java applet": "npapi-java-plugin-removal",
    "java": "npapi-java-plugin-removal",
    "quicktime": "quicktime-vr-death",
    "realplayer": "realplayer-format-abandonment",
    "realaudio": "realplayer-format-abandonment",
    "vrml": "vrml-plugin-obsolescence",
    "silverlight": "silverlight-eol",
    "director": "adobe-director-discontinued",
    "activex": "internet-explorer-retired",
    "midi": "midi-browser-playback-removed",
    "shockwave": "shockwave-player-eol",
    "3d": None,  # too generic
    "html": None,
    "javascript": None,
    "css": None,
    "perl": None,
    "php": None,
    "mp3": None,
}

# ── SPARQL ──────────────────────────────────────────────────────────────────

ARTWORKS_QUERY = """
PREFIX p: <https://artbase.rhizome.org/prop/direct/>
PREFIX e: <https://artbase.rhizome.org/entity/>

SELECT ?item ?label ?artistLabel ?inception ?url ?slug ?tags WHERE {
  ?item p:P3 e:Q5 .
  ?item rdfs:label ?label . FILTER(lang(?label) = "en")
  OPTIONAL { ?item p:P29 ?artist . ?artist rdfs:label ?artistLabel . FILTER(lang(?artistLabel) = "en") }
  OPTIONAL { ?item p:P26 ?inception }
  OPTIONAL { ?item p:P46 ?url }
  OPTIONAL { ?item p:P49 ?slug }
  OPTIONAL { ?item p:P48 ?tags }
}
"""


def sparql_query(query):
    """Execute SPARQL query and return results."""
    data = urlencode({"query": query, "format": "json"}).encode()
    req = Request(SPARQL_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("Accept", "application/json")
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


# ── Tech extraction ─────────────────────────────────────────────────────────

TECH_KEYWORDS = [
    "Flash", "Shockwave", "Java", "QuickTime", "RealPlayer", "RealAudio",
    "VRML", "Silverlight", "ActiveX", "Director", "MIDI", "Authorware",
    "SMIL", "Beatnik", "Pulse 3D", "Cosmo Player",
]

TECH_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in TECH_KEYWORDS) + r')\b',
    re.IGNORECASE
)


def extract_techs(tags_str):
    """Extract technology dependencies from legacy tags string."""
    if not tags_str:
        return []
    matches = TECH_PATTERN.findall(tags_str)
    return list(set(m.lower() for m in matches))


def tech_to_event(tech):
    """Map a technology keyword to an extinction event slug."""
    tech_lower = tech.lower()
    for key, event in TECH_TO_EVENT.items():
        if key in tech_lower:
            return event
    return None


# ── SAIA LLM ────────────────────────────────────────────────────────────────

def saia_classify(artwork_title, artist, tags, techs):
    """Use SAIA LLM to determine extinction impact for ambiguous cases."""
    if not SAIA_API_KEY:
        return None

    prompt = f"""You are an expert in digital art preservation and net art history.

Given this artwork from Rhizome's ArtBase, determine:
1. What specific technology dependencies would cause it to break?
2. What is the most likely current status: "dead", "degraded", "restored", or "unknown"?
3. What severity of impact: "total", "major", or "minor"?

Artwork: {artwork_title}
Artist: {artist}
Tags: {tags}
Detected technologies: {', '.join(techs) if techs else 'none detected'}

Respond in JSON format only:
{{"technologies": ["tech1", "tech2"], "status": "dead|degraded|restored|unknown", "severity": "total|major|minor", "reasoning": "brief explanation"}}"""

    payload = json.dumps({
        "model": SAIA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 300,
    }).encode()

    req = Request(f"{SAIA_BASE_URL}/chat/completions", data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {SAIA_API_KEY}")
    req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        content = result["choices"][0]["message"]["content"]
        # Extract JSON from response
        json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"  SAIA error: {e}", file=sys.stderr)
    return None


# ── File generation ─────────────────────────────────────────────────────────

def slugify(s):
    """Convert string to kebab-case slug."""
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'^-|-$', '', s)
    return s[:60]


def artwork_exists(slug):
    """Check if artwork already exists."""
    return (ARTWORKS_DIR / f"{slug}.md").exists()


def generate_artwork_md(item):
    """Generate artwork markdown file content."""
    lines = ["---"]
    lines.append("ai_generated: true")
    lines.append(f'title: "{item["title"].replace(chr(34), chr(92)+chr(34))}"')
    lines.append(f'artist: "{item["artist"].replace(chr(34), chr(92)+chr(34))}"')
    if item.get("year"):
        lines.append(f'year: {item["year"]}')
    if item.get("url"):
        lines.append(f'url: "{item["url"]}"')
    lines.append(f'medium: "Net art"')
    if item.get("description"):
        desc = item["description"].replace('"', '\\"')
        lines.append(f'description: "{desc}"')
    lines.append("---")
    lines.append("")
    lines.append(f'Sourced from [Rhizome ArtBase]({item["artbase_url"]}).')
    if item.get("techs"):
        lines.append(f'\nTechnology dependencies: {", ".join(item["techs"])}.')
    lines.append("")
    return "\n".join(lines)


# ── Main pipeline ───────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Querying ArtBase SPARQL endpoint...")
    result = sparql_query(ARTWORKS_QUERY)
    bindings = result["results"]["bindings"]
    print(f"  Got {len(bindings)} results")

    # Parse results
    artworks = {}
    for b in bindings:
        qid = b["item"]["value"].split("/")[-1]
        if qid in artworks:
            # Merge tags from multiple rows
            if "tags" in b:
                artworks[qid]["tags_raw"] += ", " + b["tags"]["value"]
            continue

        year = None
        if "inception" in b:
            year_match = re.match(r'(\d{4})', b["inception"]["value"])
            if year_match:
                year = int(year_match.group(1))

        artworks[qid] = {
            "qid": qid,
            "title": b["label"]["value"],
            "artist": b.get("artistLabel", {}).get("value", "Unknown"),
            "year": year,
            "url": b.get("url", {}).get("value", ""),
            "slug": b.get("slug", {}).get("value", "") or slugify(b["label"]["value"]),
            "tags_raw": b.get("tags", {}).get("value", ""),
            "artbase_url": f"https://artbase.rhizome.org/wiki/{qid}",
        }

    print(f"  Parsed {len(artworks)} unique artworks")

    # Extract technologies and find matches
    matched = []
    unmatched_with_tech = []
    no_tech = []

    for qid, art in artworks.items():
        techs = extract_techs(art["tags_raw"])
        art["techs"] = techs

        if not techs:
            no_tech.append(art)
            continue

        events = set()
        for t in techs:
            evt = tech_to_event(t)
            if evt:
                events.add(evt)

        if events:
            art["matched_events"] = list(events)
            matched.append(art)
        else:
            unmatched_with_tech.append(art)

    print(f"\n  Matched to events: {len(matched)}")
    print(f"  Has tech but no event match: {len(unmatched_with_tech)}")
    print(f"  No tech tags: {len(no_tech)}")

    # Use SAIA for artworks with tech but no direct match
    if SAIA_API_KEY and unmatched_with_tech:
        print(f"\nUsing SAIA to classify {len(unmatched_with_tech)} ambiguous artworks...")
        for i, art in enumerate(unmatched_with_tech[:50]):  # Limit to 50 for now
            print(f"  [{i+1}/{min(len(unmatched_with_tech), 50)}] {art['title'][:50]}...", end="")
            classification = saia_classify(art["title"], art["artist"], art["tags_raw"], art["techs"])
            if classification:
                art["saia_classification"] = classification
                print(f" → {classification.get('status', '?')}")
            else:
                print(" → no result")
            time.sleep(0.2)  # Rate limiting

    # Write artwork files
    new_artworks = 0
    skipped = 0
    for art in matched:
        slug = slugify(art["slug"]) or slugify(art["title"])
        if artwork_exists(slug):
            skipped += 1
            continue

        md = generate_artwork_md(art)
        outpath = ARTWORKS_DIR / f"{slug}.md"
        outpath.write_text(md)
        new_artworks += 1

    print(f"\n  New artwork files written: {new_artworks}")
    print(f"  Skipped (already exist): {skipped}")

    # Write mapping report
    report = {
        "matched": [{
            "slug": slugify(a["slug"]) or slugify(a["title"]),
            "title": a["title"],
            "artist": a["artist"],
            "techs": a["techs"],
            "events": a["matched_events"],
            "artbase_url": a["artbase_url"],
        } for a in matched],
        "ambiguous": [{
            "title": a["title"],
            "artist": a["artist"],
            "techs": a["techs"],
            "classification": a.get("saia_classification"),
            "artbase_url": a["artbase_url"],
        } for a in unmatched_with_tech],
        "stats": {
            "total_artworks": len(artworks),
            "matched": len(matched),
            "ambiguous": len(unmatched_with_tech),
            "no_tech": len(no_tech),
            "new_files": new_artworks,
        }
    }

    report_path = OUTPUT_DIR / "artbase-mapping.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\n  Mapping report: {report_path}")

    # Summary of event matches
    event_counts = {}
    for art in matched:
        for evt in art["matched_events"]:
            event_counts[evt] = event_counts.get(evt, 0) + 1

    print("\n  Event match distribution:")
    for evt, count in sorted(event_counts.items(), key=lambda x: -x[1]):
        print(f"    {count:>4}  {evt}")


if __name__ == "__main__":
    main()
