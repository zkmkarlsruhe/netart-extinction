#!/usr/bin/env python3
"""
Ingest artworks from new/expanded JSON sources into src/content/artworks/.

Handles: NTT ICC, Ars Electronica (full), Turbulence (expanded), Archive.org
Skips artworks that already have .md files (by slug).
"""

import json
import re
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARTWORKS_DIR = PROJECT_ROOT / "src" / "content" / "artworks"


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s[:80] if s else "untitled"


def escape_yaml(value) -> str:
    """Escape a string for YAML double-quoted scalar."""
    if not value:
        return ""
    value = str(value)
    value = re.sub(r"\s+", " ", value).strip()
    value = value.replace("\\", "\\\\")
    # Remove quotes rather than escape them (safer for YAML)
    value = value.replace('"', "'")
    return value


def truncate_description(desc: str, max_len: int = 160) -> str:
    """Truncate description to max_len chars."""
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) <= max_len:
        return desc
    return desc[:max_len].rsplit(" ", 1)[0]


def generate_md(item: dict, source_name: str, source_label: str) -> str:
    """Generate markdown content for an artwork."""
    lines = ["---"]
    lines.append("ai_generated: true")

    title = escape_yaml(item.get("title", "Untitled"))
    lines.append(f'title: "{title}"')

    artist = escape_yaml(item.get("artist", "Unknown"))
    lines.append(f'artist: "{artist}"')

    year = item.get("year")
    if isinstance(year, int) and 1900 <= year <= 2030:
        lines.append(f"year: {year}")

    url = item.get("url", "")
    if url and url.startswith("http"):
        lines.append(f'url: "{escape_yaml(url)}"')

    medium = item.get("medium", "Net art")
    lines.append(f'medium: "{escape_yaml(medium)}"')

    desc = item.get("description", "")
    if desc:
        truncated = truncate_description(desc)
        lines.append(f'description: "{escape_yaml(truncated)}"')

    lines.append("---")
    lines.append("")

    # Source attribution
    source_url = item.get("source_url", "")
    if source_url:
        lines.append(f"Sourced from [{source_label}]({source_url}).")
    else:
        lines.append(f"Sourced from {source_name}.")

    # Award info (Ars Electronica)
    award = item.get("award", "")
    category = item.get("category", "")
    if award and category:
        lines.append(f"Award: {award} ({category}).")
    elif award:
        lines.append(f"Award: {award}.")

    # Technologies
    techs = item.get("technologies", [])
    if techs:
        lines.append(f"\nTechnology dependencies: {', '.join(techs)}.")

    lines.append("")
    return "\n".join(lines)


def ingest_source(json_path: str, source_name: str, source_label: str) -> tuple[int, int]:
    """Ingest a single source. Returns (created, skipped) counts."""
    path = PROJECT_ROOT / json_path
    if not path.exists():
        print(f"  SKIP: {json_path} not found")
        return 0, 0

    with open(path) as f:
        data = json.load(f)

    created = 0
    skipped = 0
    seen_slugs = set()

    for item in data:
        title = item.get("title", "").strip()
        if not title:
            skipped += 1
            continue

        slug = slugify(title)
        if not slug or slug == "untitled":
            skipped += 1
            continue

        # Dedupe within this batch
        if slug in seen_slugs:
            skipped += 1
            continue
        seen_slugs.add(slug)

        md_path = ARTWORKS_DIR / f"{slug}.md"
        if md_path.exists():
            skipped += 1
            continue

        content = generate_md(item, source_name, source_label)
        md_path.write_text(content, encoding="utf-8")
        created += 1

    return created, skipped


def main():
    ARTWORKS_DIR.mkdir(parents=True, exist_ok=True)

    sources = [
        ("data/sources/ntt-icc/artworks.json", "ntt-icc", "NTT ICC"),
        ("data/sources/ars-electronica/artworks-all.json", "ars-electronica", "Ars Electronica Prix"),
        ("data/sources/turbulence/artworks.json", "turbulence", "Turbulence.org"),
        ("data/sources/archive-org/artworks.json", "archive-org", "Archive.org"),
        ("data/sources/lima/artworks.json", "lima", "LIMA"),
        ("data/sources/media-art-net/artworks.json", "media-art-net", "Media Art Net"),
        ("data/sources/computerfinearts/artworks.json", "computerfinearts", "Computer Fine Arts"),
        ("data/sources/dia/artworks.json", "dia", "Dia Art Foundation"),
        ("data/sources/runme/artworks.json", "runme", "Runme.org"),
    ]

    total_created = 0
    total_skipped = 0

    for json_path, source_name, source_label in sources:
        created, skipped = ingest_source(json_path, source_name, source_label)
        total_created += created
        total_skipped += skipped
        print(f"  {source_label}: {created} created, {skipped} skipped")

    print(f"\nTotal: {total_created} created, {total_skipped} skipped")


if __name__ == "__main__":
    main()
