# Net Art Extinction Timeline

[![ZKM](https://img.shields.io/badge/ZKM-Karlsruhe-blue)](https://zkm.de)
[![ZKM Open Source](https://img.shields.io/badge/ZKM-Open%20Source-blue)](https://github.com/zkmkarlsruhe)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19254683.svg)](https://doi.org/10.5281/zenodo.19254683)

Documenting how dependency changes — API shutdowns, plugin end-of-lifes, browser removals — break digital artworks.

**Live site:** [extinction.zkm.de](https://extinction.zkm.de)

## Quick start

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # Static output in dist/
npm run preview  # Preview production build
```

## Architecture

- **Framework:** [Astro](https://astro.build) (static site generation)
- **Visualization:** D3.js (client-side SVG timeline)
- **Content:** Markdown files with validated frontmatter (Astro Content Collections)
- **Hosting:** Docker (nginx)

### Directory structure

```
src/
  content/
    events/       # Extinction event entries (Markdown + frontmatter)
    artworks/     # Artwork entries (Markdown + frontmatter)
  components/
    timeline/     # D3 timeline visualization
    ui/           # Shared UI components (badges, cards, header, footer)
  layouts/        # Base HTML layout
  lib/            # Utilities (date parsing)
  pages/          # Astro page routes
  styles/         # Global CSS + timeline styles
```

### Content model

**Events** document a specific dependency change (e.g., "Flash Player blocked"). Each event references zero or more **artworks** that were affected, with per-artwork severity and status.

**Artworks** are canonical records of digital works (title, artist, year, URL, medium).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add events and artworks.

## License

Content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: [MIT](https://opensource.org/licenses/MIT).

An official open-source project of [ZKM | Zentrum für Kunst und Medien Karlsruhe](https://zkm.de),
developed and maintained by Marc Schütze. Companion project: [vmctl](https://vmctl.org) — reviving
born-digital art on faithful period virtual machines.
