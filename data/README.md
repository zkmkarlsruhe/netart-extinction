# Data Sources

Raw scraped/queried data from external archives. Each source gets its own directory with the original data in JSON format, so we can re-ingest without re-scraping.

## Structure

```
data/
  sources/
    artbase/          # Rhizome ArtBase (SPARQL)
    whitney/          # Whitney Artport (HTML scrape)
    ars-electronica/  # Ars Electronica Prix (AJAX endpoints)
    turbulence/       # Turbulence.org (Wayback Machine)
    lima/             # LIMA / mediakunst.net (REST API)
    ntt-icc/          # NTT ICC Tokyo (HTML scrape)
    ada/              # Archive of Digital Art (contact/scrape)
```

## File conventions

Each source directory contains:
- `artworks.json` — normalized artwork records
- `raw/` — original API responses or scraped HTML (optional)
- `README.md` — access notes, date scraped, any auth requirements

## Normalized artwork format

```json
{
  "source": "artbase",
  "source_id": "Q1234",
  "source_url": "https://artbase.rhizome.org/wiki/Q1234",
  "title": "Artwork Title",
  "artist": "Artist Name",
  "year": 2001,
  "url": "https://original-artwork-url.com",
  "medium": "Net art",
  "technologies": ["Flash", "Shockwave"],
  "description": "...",
  "preservation": {
    "status": "dead|degraded|restored|working|unknown",
    "archive_url": "https://archive.example.com/...",
    "notes": ""
  }
}
```
