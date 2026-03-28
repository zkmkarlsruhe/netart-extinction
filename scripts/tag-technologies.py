#!/usr/bin/env python3
"""
Detect and tag technologies in artwork frontmatter based on:
- Source JSON technology fields
- ArtBase SPARQL tags
- URL patterns (e.g. .swf, .jar)
- Title/description keyword matching
- Body text mentions

Writes `technologies:` array into artwork .md frontmatter.
"""

import json
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTWORKS_DIR = PROJECT_ROOT / "src" / "content" / "artworks"
CORPUS_FILE = PROJECT_ROOT / "data" / "corpus" / "netart-corpus.json"
ARTBASE_FILE = PROJECT_ROOT / "data" / "sources" / "artbase" / "artworks.json"
TECH_MAPPING_FILE = PROJECT_ROOT / "data" / "sources" / "artbase" / "tech-mapping.json"

# ── Technology detection patterns ──────────────────────────────────────────

# Keywords to detect in titles, descriptions, URLs, body text
# Maps pattern → canonical technology name
TECH_PATTERNS = {
    # Plugins / runtimes
    r'\bflash\b': 'Flash',
    r'\bshockwave\b': 'Shockwave',
    r'\bmacromedia\b': 'Flash',
    r'\b\.swf\b': 'Flash',
    r'\bjava\s*applet': 'Java Applet',
    r'\b\.jar\b': 'Java Applet',
    r'\bquicktime\b': 'QuickTime',
    r'\b\.mov\b': 'QuickTime',
    r'\brealplayer\b': 'RealPlayer',
    r'\brealaudio\b': 'RealAudio',
    r'\b\.ram?\b': 'RealAudio',
    r'\bvrml\b': 'VRML',
    r'\b\.wrl\b': 'VRML',
    r'\bsilverlight\b': 'Silverlight',
    r'\bdirector\b(?!\s+(of|at|for))': 'Macromedia Director',
    r'\bactivex\b': 'ActiveX',
    r'\bauthorware\b': 'Authorware',

    # Formats / protocols
    r'\bmidi\b': 'MIDI',
    r'\b\.mid\b': 'MIDI',
    r'\bsmil\b': 'SMIL',

    # Languages / frameworks
    r'\bjavascript\b': 'JavaScript',
    r'\bjquery\b': 'JavaScript',
    r'\bhtml5?\b': 'HTML',
    r'\bcss\b': 'CSS',
    r'\bwebgl\b': 'WebGL',
    r'\bthree\.js\b': 'WebGL',
    r'\bp5\.js\b': 'p5.js',
    r'\bprocessing\b': 'Processing',
    r'\bopenframeworks\b': 'openFrameworks',
    r'\bpython\b': 'Python',
    r'\bperl\b': 'Perl',
    r'\bphp\b': 'PHP',
    r'\bcgi\b': 'CGI',
    r'\bmysql\b': 'MySQL',

    # Platforms
    r'\bsecond\s*life\b': 'Second Life',
    r'\bunity\b': 'Unity',
    r'\bunreal\b': 'Unreal Engine',
    r'\barduin[oa]\b': 'Arduino',
    r'\braspberry\s*pi\b': 'Raspberry Pi',
    r'\bmax/msp\b': 'Max/MSP',
    r'\bmax\s*msp\b': 'Max/MSP',
    r'\bpure\s*data\b': 'Pure Data',
    r'\bsupercollider\b': 'SuperCollider',

    # Video / streaming
    r'\bmpeg\b': 'MPEG',
    r'\bmp4\b': 'MP4',
    r'\bavi\b': 'AVI',
    r'\bwmv\b': 'WMV',
    r'\bmp3\b': 'MP3',
    r'\bwav\b': 'WAV',

    # 3D
    r'\bx3d\b': 'X3D',
    r'\b3d\s*studio\b': '3D Studio',
    r'\bmaya\b(?!\s+(angelou|deren))': 'Maya',
    r'\bblender\b': 'Blender',

    # AI / ML
    r'\bgenerative\s*adversarial\b': 'GAN',
    r'\bneural\s*network\b': 'Neural Network',
    r'\bmachine\s*learning\b': 'Machine Learning',
    r'\btensorflow\b': 'TensorFlow',
    r'\bgpt\b': 'GPT',

    # OS-specific
    r'\bwindows\s*(\d+|xp|vista)\b': 'Windows',
    r'\bmacos\b': 'macOS',
    r'\blinux\b': 'Linux',
    r'\bios\b(?!\s)': 'iOS',
    r'\bandroid\b': 'Android',
}

# Build compiled patterns
COMPILED_PATTERNS = [
    (re.compile(pattern, re.IGNORECASE), tech)
    for pattern, tech in TECH_PATTERNS.items()
]

# Known tags from ArtBase → tech mapping
ARTBASE_TAG_MAP = {
    'flash': 'Flash',
    'shockwave': 'Shockwave',
    'java': 'Java Applet',
    'java applet': 'Java Applet',
    'quicktime': 'QuickTime',
    'realplayer': 'RealPlayer',
    'realaudio': 'RealAudio',
    'vrml': 'VRML',
    'silverlight': 'Silverlight',
    'director': 'Macromedia Director',
    'activex': 'ActiveX',
    'midi': 'MIDI',
    'authorware': 'Authorware',
    'javascript': 'JavaScript',
    'html': 'HTML',
    'css': 'CSS',
    'php': 'PHP',
    'perl': 'Perl',
    'python': 'Python',
    'cgi': 'CGI',
    'mysql': 'MySQL',
    'webgl': 'WebGL',
    'processing': 'Processing',
    'arduino': 'Arduino',
    'max/msp': 'Max/MSP',
    'pure data': 'Pure Data',
    'unity': 'Unity',
    'second life': 'Second Life',
    'smil': 'SMIL',
    'svg': 'SVG',
    'xml': 'XML',
    'ajax': 'AJAX',
    'asp': 'ASP',
    'coldfusion': 'ColdFusion',
    'beatnik': 'Beatnik',
    'pulse 3d': 'Pulse 3D',
    'ipix': 'iPIX',
    'cosmo player': 'VRML',
}


def detect_techs_from_text(text: str) -> set[str]:
    """Detect technologies from a text string using regex patterns."""
    techs = set()
    for pattern, tech in COMPILED_PATTERNS:
        if pattern.search(text):
            techs.add(tech)
    return techs


def load_corpus_techs() -> dict[str, list[str]]:
    """Load technology data from corpus (keyed by normalized title)."""
    if not CORPUS_FILE.exists():
        return {}
    corpus = json.loads(CORPUS_FILE.read_text())
    result = {}
    for record in corpus:
        techs = record.get("technologies", [])
        if techs:
            key = re.sub(r"[^a-z0-9]+", " ", record["title"].lower()).strip()
            result[key] = [ARTBASE_TAG_MAP.get(t.lower(), t) for t in techs]
    return result


def load_artbase_techs() -> dict[str, list[str]]:
    """Load technology tags from ArtBase source data."""
    if not ARTBASE_FILE.exists():
        return {}
    data = json.loads(ARTBASE_FILE.read_text())
    result = {}
    for item in data:
        tags = item.get("tags", [])
        if not tags:
            continue
        techs = []
        for tag in (tags if isinstance(tags, list) else [tags]):
            tag_lower = str(tag).lower().strip()
            if tag_lower in ARTBASE_TAG_MAP:
                techs.append(ARTBASE_TAG_MAP[tag_lower])
        if techs:
            slug = slugify(item.get("title", ""))
            if slug:
                result[slug] = techs
    return result


def load_tech_mapping() -> dict[str, list[str]]:
    """Load from the existing tech-mapping.json (SAIA classified)."""
    if not TECH_MAPPING_FILE.exists():
        return {}
    data = json.loads(TECH_MAPPING_FILE.read_text())
    result = {}
    for item in data.get("matched", []):
        slug = item.get("slug", "")
        techs = [ARTBASE_TAG_MAP.get(t.lower(), t) for t in item.get("techs", [])]
        if slug and techs:
            result[slug] = techs
    return result


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s[:80] if s else ""


def parse_frontmatter(text: str) -> tuple[str, str]:
    """Split into frontmatter text and body."""
    if not text.startswith("---"):
        return "", text
    end = text.index("---", 3)
    return text[3:end].strip(), text[end + 3:]


def add_technologies_to_md(filepath: Path, techs: list[str]) -> bool:
    """Add technologies array to artwork frontmatter. Returns True if modified."""
    text = filepath.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    if "technologies:" in fm:
        return False  # Already has technologies

    # Insert before ai_generated or at end of frontmatter
    tech_yaml = "technologies:\n" + "\n".join(f'  - "{t}"' for t in sorted(set(techs)))

    if "ai_generated:" in fm:
        fm = fm.replace("ai_generated:", f"{tech_yaml}\nai_generated:")
    else:
        fm = fm + "\n" + tech_yaml

    new_text = f"---\n{fm}\n---{body}"
    filepath.write_text(new_text, encoding="utf-8")
    return True


def main():
    # Load pre-existing tech data from various sources
    corpus_techs = load_corpus_techs()
    artbase_techs = load_artbase_techs()
    mapping_techs = load_tech_mapping()

    print(f"Corpus tech records: {len(corpus_techs)}")
    print(f"ArtBase tag records: {len(artbase_techs)}")
    print(f"SAIA mapping records: {len(mapping_techs)}")

    tagged = 0
    scanned = 0

    for md_file in sorted(ARTWORKS_DIR.glob("*.md")):
        scanned += 1
        text = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        if "technologies:" in fm:
            continue  # Already tagged

        slug = md_file.stem
        techs = set()

        # 1. Check pre-existing sources
        if slug in mapping_techs:
            techs.update(mapping_techs[slug])
        if slug in artbase_techs:
            techs.update(artbase_techs[slug])

        # Normalize title for corpus lookup
        title_match = re.search(r'title:\s*"(.+?)"', fm)
        if title_match:
            title_key = re.sub(r"[^a-z0-9]+", " ", title_match.group(1).lower()).strip()
            if title_key in corpus_techs:
                techs.update(corpus_techs[title_key])

        # 2. Detect from frontmatter text (title, description, url, medium)
        techs.update(detect_techs_from_text(fm))

        # 3. Detect from body text
        techs.update(detect_techs_from_text(body))

        # Skip very generic detections if that's the only signal
        # (HTML/CSS/JavaScript are too common to be interesting alone)
        interesting = techs - {"HTML", "CSS", "JavaScript"}
        if not interesting and techs:
            # Only tag if we have something beyond basic web tech
            # Unless it came from a curated source
            if slug not in mapping_techs and slug not in artbase_techs:
                continue

        if techs:
            if add_technologies_to_md(md_file, list(techs)):
                tagged += 1

    print(f"\nScanned: {scanned}")
    print(f"Tagged: {tagged}")


if __name__ == "__main__":
    main()
