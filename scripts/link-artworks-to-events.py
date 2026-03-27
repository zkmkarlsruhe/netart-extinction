#!/usr/bin/env python3
"""
Link ArtBase artworks to extinction events by adding affected_artworks
entries to event frontmatter.
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
EVENTS_DIR = PROJECT_ROOT / "src" / "content" / "events"
ARTWORKS_DIR = PROJECT_ROOT / "src" / "content" / "artworks"
MAPPING_FILE = PROJECT_ROOT / "scripts" / "output" / "artbase-mapping.json"


def parse_frontmatter(text):
    """Split file into frontmatter dict lines and body."""
    if not text.startswith("---"):
        return [], text
    end = text.index("---", 3)
    fm = text[3:end].strip()
    body = text[end + 3:].lstrip("\n")
    return fm, body


def get_existing_artwork_refs(fm_text):
    """Extract already-linked artwork slugs from frontmatter."""
    refs = set()
    in_affected = False
    for line in fm_text.split("\n"):
        if line.strip().startswith("affected_artworks:"):
            in_affected = True
            continue
        if in_affected:
            if line.strip().startswith("- artwork:"):
                slug = line.strip().split("artwork:")[1].strip().strip('"')
                refs.add(slug)
            elif line.strip().startswith("-") and "artwork" not in line:
                continue
            elif not line.startswith(" ") and not line.startswith("\t") and line.strip():
                in_affected = False
    return refs


def build_affected_block(slugs):
    """Build YAML block for affected_artworks entries."""
    lines = []
    for slug in sorted(slugs):
        lines.append(f'  - artwork: "{slug}"')
        lines.append(f"    severity: total")
        lines.append(f"    status: dead")
    return "\n".join(lines)


def main():
    mapping = json.loads(MAPPING_FILE.read_text())

    # Group artworks by event
    event_artworks = {}
    for art in mapping["matched"]:
        slug = art["slug"]
        # Verify artwork file exists
        if not (ARTWORKS_DIR / f"{slug}.md").exists():
            continue
        for evt in art["events"]:
            if evt not in event_artworks:
                event_artworks[evt] = []
            event_artworks[evt].append(slug)

    print(f"Events to update: {len(event_artworks)}")

    for event_slug, new_slugs in event_artworks.items():
        event_file = EVENTS_DIR / f"{event_slug}.md"
        if not event_file.exists():
            print(f"  SKIP {event_slug} — file not found")
            continue

        text = event_file.read_text()
        fm, body = parse_frontmatter(text)

        # Get existing refs
        existing = get_existing_artwork_refs(fm)
        to_add = [s for s in new_slugs if s not in existing]

        if not to_add:
            print(f"  {event_slug}: all {len(new_slugs)} already linked")
            continue

        # Check if affected_artworks section exists
        if "affected_artworks:" in fm:
            # Append new entries before the next top-level key or end of frontmatter
            lines = fm.split("\n")
            new_lines = []
            in_affected = False
            inserted = False

            for i, line in enumerate(lines):
                new_lines.append(line)
                if line.strip() == "affected_artworks:":
                    in_affected = True
                    continue
                if in_affected:
                    # Check if next line is a new top-level key or we're at end
                    is_nested = line.startswith(" ") or line.startswith("\t") or line.strip() == ""
                    next_is_toplevel = (i + 1 < len(lines) and
                                       not lines[i + 1].startswith(" ") and
                                       not lines[i + 1].startswith("\t") and
                                       lines[i + 1].strip() != "" and
                                       not lines[i + 1].strip().startswith("-"))

                    if not is_nested or next_is_toplevel or i == len(lines) - 1:
                        # Insert new entries here
                        new_lines.append(build_affected_block(to_add))
                        in_affected = False
                        inserted = True

            if not inserted:
                new_lines.append(build_affected_block(to_add))

            fm = "\n".join(new_lines)
        else:
            # Add new affected_artworks section
            fm += "\naffected_artworks:\n" + build_affected_block(to_add)

        # Reconstruct file
        new_text = f"---\n{fm}\n---\n\n{body}"
        event_file.write_text(new_text)
        print(f"  {event_slug}: added {len(to_add)} artworks (had {len(existing)})")

    print("\nDone!")


if __name__ == "__main__":
    main()
