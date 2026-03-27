#!/usr/bin/env python3
"""
Use SAIA LLM to classify ArtBase artworks that have no technology tags.
Also queries preservation status from ArtBase variants to set correct status.

Pipeline:
1. Query all artworks + their variant archive URLs from ArtBase
2. For artworks already matched by tech tags, update status if archived
3. For untagged artworks, use SAIA to classify technology
4. Create artwork files and link to events
"""

import json
import os
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode

SPARQL_URL = "https://query.artbase.rhizome.org/proxy/wdqs/bigdata/namespace/wdq/sparql"
SAIA_BASE_URL = os.environ.get("SAIA_BASE_URL", "https://chat-ai.academiccloud.de/v1")
SAIA_API_KEY = os.environ.get("SAIA_API_KEY", "")
SAIA_MODEL = "mistral-large-3-675b-instruct-2512"

PROJECT_ROOT = Path(__file__).parent.parent
ARTWORKS_DIR = PROJECT_ROOT / "src" / "content" / "artworks"
EVENTS_DIR = PROJECT_ROOT / "src" / "content" / "events"
OUTPUT_DIR = PROJECT_ROOT / "scripts" / "output"

TECH_KEYWORDS = [
    "Flash", "Shockwave", "Java", "QuickTime", "RealPlayer", "RealAudio",
    "VRML", "Silverlight", "ActiveX", "Director", "MIDI", "Authorware",
    "SMIL", "Beatnik", "Pulse 3D",
]
TECH_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in TECH_KEYWORDS) + r')\b',
    re.IGNORECASE
)

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
    "authorware": "macromedia-authorware-format-death",
    "smil": "smil-browser-support-collapse",
}


def sparql_query(query):
    data = urlencode({"query": query, "format": "json"}).encode()
    req = Request(SPARQL_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def saia_classify(title, artist, year, url, tags):
    prompt = f"""You are an expert in net art and digital preservation.

Analyze this artwork from Rhizome's ArtBase and determine what technology it depends on.

Title: {title}
Artist: {artist}
Year: {year or "unknown"}
URL: {url or "not available"}
Tags: {tags or "none"}

Only identify technologies that are now obsolete (Flash, Shockwave, Java applets, QuickTime, RealPlayer, VRML, Silverlight, ActiveX, Director, MIDI, Authorware, SMIL).
If the artwork likely uses only HTML/CSS/JavaScript (still works), respond with empty tech list.

Respond ONLY with JSON:
{{"likely_tech": ["tech1"], "likely_status": "dead|degraded|working|unknown", "confidence": "high|medium|low", "reasoning": "brief"}}"""

    payload = json.dumps({
        "model": SAIA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1, "max_tokens": 200,
    }).encode()

    req = Request(f"{SAIA_BASE_URL}/chat/completions", data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {SAIA_API_KEY}")
    req.add_header("Content-Type", "application/json")

    with urlopen(req, timeout=30) as resp:
        r = json.loads(resp.read())
    content = r["choices"][0]["message"]["content"]
    jm = re.search(r'\{[^}]+\}', content, re.DOTALL)
    if jm:
        return json.loads(jm.group())
    return None


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'^-|-$', '', s)
    return s[:60]


def generate_artwork_md(title, artist, year, url, qid, techs, archive_url=None):
    lines = ["---", "ai_generated: true"]
    lines.append(f'title: "{title.replace(chr(34), chr(92)+chr(34))}"')
    lines.append(f'artist: "{artist.replace(chr(34), chr(92)+chr(34))}"')
    if year:
        lines.append(f'year: {year}')
    if url:
        lines.append(f'url: "{url}"')
    lines.append('medium: "Net art"')
    lines.append("---")
    lines.append("")
    lines.append(f'Sourced from [Rhizome ArtBase](https://artbase.rhizome.org/wiki/{qid}).')
    if techs:
        lines.append(f'\nTechnology dependencies: {", ".join(techs)}.')
    if archive_url:
        lines.append(f'\nPreserved copy: [{archive_url}]({archive_url})')
    lines.append("")
    return "\n".join(lines)


def update_artwork_status(slug, new_status):
    """Update status in event files for a given artwork slug."""
    for ef in EVENTS_DIR.glob("*.md"):
        text = ef.read_text()
        if f'artwork: "{slug}"' not in text:
            continue
        # Find and replace status for this artwork
        pattern = f'(artwork: "{slug}"\\n    severity: \\w+\\n    status: )\\w+'
        new_text = re.sub(pattern, f'\\g<1>{new_status}', text)
        if new_text != text:
            ef.write_text(new_text)


def add_to_event(event_slug, artwork_slug, status="dead"):
    """Add artwork to event's affected_artworks."""
    event_file = EVENTS_DIR / f"{event_slug}.md"
    if not event_file.exists():
        return False

    text = event_file.read_text()
    if f'artwork: "{artwork_slug}"' in text:
        return False

    entry = f'  - artwork: "{artwork_slug}"\n    severity: total\n    status: {status}'

    if "affected_artworks:" in text:
        lines = text.split("\n")
        last_idx = -1
        for i, line in enumerate(lines):
            if re.match(r'\s+- artwork:', line):
                last_idx = i
        if last_idx >= 0:
            insert_idx = last_idx + 1
            while insert_idx < len(lines) and lines[insert_idx].startswith("    "):
                insert_idx += 1
            lines.insert(insert_idx, entry)
            text = "\n".join(lines)
    else:
        fm_end = text.index("---", 3)
        text = text[:fm_end] + "affected_artworks:\n" + entry + "\n" + text[fm_end:]

    event_file.write_text(text)
    return True


def main():
    if not SAIA_API_KEY:
        print("ERROR: Set SAIA_API_KEY environment variable")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ── Step 1: Query all artworks + preservation data ──────────────────
    print("Querying ArtBase artworks...")
    result = sparql_query("""
        PREFIX p: <https://artbase.rhizome.org/prop/direct/>
        PREFIX e: <https://artbase.rhizome.org/entity/>
        SELECT ?item ?label ?artistLabel ?inception ?url ?slug ?tags WHERE {
          ?item p:P3 e:Q5 .
          ?item rdfs:label ?label . FILTER(lang(?label) = "en")
          OPTIONAL { ?item p:P29 ?a . ?a rdfs:label ?artistLabel . FILTER(lang(?artistLabel) = "en") }
          OPTIONAL { ?item p:P26 ?inception }
          OPTIONAL { ?item p:P46 ?url }
          OPTIONAL { ?item p:P49 ?slug }
          OPTIONAL { ?item p:P48 ?tags }
        }
    """)

    artworks = {}
    for b in result["results"]["bindings"]:
        qid = b["item"]["value"].split("/")[-1]
        if qid not in artworks:
            year = None
            if "inception" in b:
                m = re.match(r'(\d{4})', b["inception"]["value"])
                if m: year = int(m.group(1))
            artworks[qid] = {
                "qid": qid, "title": b["label"]["value"],
                "artist": b.get("artistLabel", {}).get("value", "Unknown"),
                "year": year, "url": b.get("url", {}).get("value", ""),
                "slug": b.get("slug", {}).get("value", ""),
                "tags": b.get("tags", {}).get("value", ""),
                "archive_urls": [],
            }
        elif "tags" in b:
            artworks[qid]["tags"] += ", " + b["tags"]["value"]

    print(f"  {len(artworks)} artworks")

    # ── Step 2: Query preservation (archived variants) ──────────────────
    print("Querying preservation data...")
    pres_result = sparql_query("""
        PREFIX p: <https://artbase.rhizome.org/prop/direct/>
        PREFIX e: <https://artbase.rhizome.org/entity/>
        SELECT ?artwork ?variantUrl WHERE {
          ?artwork p:P3 e:Q5 .
          ?artwork p:P45 ?variant .
          ?variant p:P46 ?variantUrl .
          FILTER(CONTAINS(STR(?variantUrl), "archive.rhizome.org") ||
                 CONTAINS(STR(?variantUrl), "conifer.rhizome.org") ||
                 CONTAINS(STR(?variantUrl), "oldweb.today") ||
                 CONTAINS(STR(?variantUrl), "variants.artbase"))
        }
    """)

    preserved_qids = set()
    for b in pres_result["results"]["bindings"]:
        qid = b["artwork"]["value"].split("/")[-1]
        url = b["variantUrl"]["value"]
        preserved_qids.add(qid)
        if qid in artworks:
            artworks[qid]["archive_urls"].append(url)

    print(f"  {len(preserved_qids)} artworks have preservation copies")

    # ── Step 3: Update existing artwork files with preservation status ──
    print("\nUpdating preservation status for existing artworks...")
    updated_status = 0
    for qid in preserved_qids:
        if qid not in artworks:
            continue
        art = artworks[qid]
        slug = slugify(art["slug"] or art["title"])
        art_file = ARTWORKS_DIR / f"{slug}.md"
        if art_file.exists():
            update_artwork_status(slug, "restored")
            updated_status += 1
    print(f"  Updated {updated_status} artworks to 'restored'")

    # ── Step 4: SAIA classification of untagged artworks ────────────────
    no_tech = [a for a in artworks.values() if not TECH_PATTERN.findall(a["tags"])]
    print(f"\nUntagged artworks to classify: {len(no_tech)}")

    # Load checkpoint
    results_file = OUTPUT_DIR / "saia-full-classifications.json"
    if results_file.exists():
        all_results = json.loads(results_file.read_text())
        classified_qids = {r["qid"] for r in all_results}
        print(f"  Resuming from checkpoint: {len(all_results)} already done")
    else:
        all_results = []
        classified_qids = set()

    todo = [a for a in no_tech if a["qid"] not in classified_qids]
    print(f"  Remaining: {len(todo)}")

    new_artworks = 0
    new_links = 0
    errors = 0

    for i, art in enumerate(todo):
        is_preserved = art["qid"] in preserved_qids
        print(f'[{i+1:4d}/{len(todo)}] {art["title"][:40]:40s}', end="", flush=True)

        try:
            cls = saia_classify(art["title"], art["artist"], art["year"], art["url"], art["tags"])
            if cls:
                cls["qid"] = art["qid"]
                cls["artwork"] = art["title"]
                cls["artist"] = art.get("artist", "Unknown")
                cls["preserved"] = is_preserved
                all_results.append(cls)

                techs = cls.get("likely_tech", [])
                status = cls.get("likely_status", "unknown")
                conf = cls.get("confidence", "?")

                # Override status if preserved
                if is_preserved and status == "dead":
                    status = "restored"
                    cls["likely_status"] = "restored"

                print(f" | {status:10s} | {str(techs):30s} | {conf}{'  [archived]' if is_preserved else ''}", flush=True)

                # Create artwork + link if dead/degraded/restored with extinct tech
                if status in ("dead", "degraded", "restored") and conf in ("high", "medium") and techs:
                    events = set()
                    extinct_techs = []
                    for t in techs:
                        t_lower = t.lower()
                        for key, evt in TECH_TO_EVENT.items():
                            if key in t_lower:
                                extinct_techs.append(t)
                                events.add(evt)
                                break

                    if extinct_techs and events:
                        slug = slugify(art["slug"] or art["title"])
                        if not (ARTWORKS_DIR / f"{slug}.md").exists():
                            archive_url = art["archive_urls"][0] if art["archive_urls"] else None
                            md = generate_artwork_md(
                                art["title"], art["artist"], art["year"],
                                art["url"], art["qid"], extinct_techs, archive_url
                            )
                            (ARTWORKS_DIR / f"{slug}.md").write_text(md)
                            new_artworks += 1

                        for evt in events:
                            if add_to_event(evt, slug, status):
                                new_links += 1
            else:
                print(" | parse error", flush=True)
        except Exception as e:
            errors += 1
            print(f" | ERROR: {e}", flush=True)

        # Checkpoint every 50
        if (i + 1) % 50 == 0:
            results_file.write_text(json.dumps(all_results, indent=2))
            print(f"  [checkpoint: {len(all_results)} classified, {new_artworks} new, {new_links} links]", flush=True)

        time.sleep(0.2)

    # Final save
    results_file.write_text(json.dumps(all_results, indent=2))

    # ── Summary ─────────────────────────────────────────────────────────
    from collections import Counter
    statuses = Counter(r.get("likely_status") for r in all_results)
    all_techs = Counter(t for r in all_results for t in r.get("likely_tech", []))
    preserved_count = sum(1 for r in all_results if r.get("preserved"))

    print(f"\n{'='*60}")
    print(f"Total classified: {len(all_results)}")
    print(f"New artwork files: {new_artworks}")
    print(f"New event links: {new_links}")
    print(f"Status updated to restored: {updated_status}")
    print(f"With preservation copies: {preserved_count}")
    print(f"Errors: {errors}")
    print(f"\nStatus distribution: {dict(statuses)}")
    print(f"\nTop technologies:")
    for tech, count in all_techs.most_common(15):
        print(f"  {count:>4}  {tech}")


if __name__ == "__main__":
    main()
