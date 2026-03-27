# Contributing

We welcome contributions documenting extinction events and affected artworks. There are two ways to contribute.

## 1. GitHub Issue Form (easiest)

Use our structured forms — no technical knowledge required:

- [Report an extinction event or affected artwork](https://github.com/zkmkarlsruhe/netart-extinction/issues/new/choose)

A maintainer will review your submission, and a PR will be auto-generated.

## 2. Pull Request

Fork the repo and add a Markdown file directly.

### Adding an artwork

Create `src/content/artworks/your-artwork-slug.md`:

```markdown
---
title: "Artwork Title"
artist: "Artist Name"
year: 2008
url: "https://example.com"
medium: "Web application"
description: "Brief description of what the artwork is."
---

Optional body text with additional context about the artwork.
```

### Adding an event

Create `src/content/events/your-event-slug.md`:

```markdown
---
title: "Event Title"
date: "2023-02-09"
dependency: "Name of the dependency that changed"
event_type: "api-shutdown"
summary: "One-sentence summary of what happened and why it matters."
links:
  - url: "https://example.com/announcement"
    label: "Official announcement"
affected_artworks:
  - artwork: your-artwork-slug
    severity: total
    status: dead
    note: "Optional note about how this artwork was specifically affected."
fixes:
  - type: none
    description: "Description of available fix or why no fix exists."
---

## What changed

Longer narrative about what happened.

## Notes

Additional context.
```

### Field reference

**`date`**: Flexible format — `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`.

**`event_type`**: One of: `api-shutdown`, `plugin-eol`, `browser-change`, `platform-shutdown`, `protocol-change`, `corporate-acquisition`, `terms-of-service`, `hardware-obsolescence`, `sdk-deprecation`, `os-deprecation`, `certificate-expiry`, `data-loss`, `format-obsolescence`, `network-shutdown`, `other`.

**`severity`** (per artwork): `total` (work is non-functional), `major` (significant degradation), `minor` (partial impact).

**`status`** (per artwork): `dead`, `degraded`, `restored`, `unknown`.

**`fix type`**: `migration`, `emulation`, `archive`, `workaround`, `rebuild`, `none`.

### File naming

Use kebab-case slugs: `twitter-api-v1-shutdown.md`, `abstract-browsing.md`.

### Validation

Run `npm run build` before submitting. Astro will validate all frontmatter against the schema — if your file has errors, the build will fail with a descriptive message.

