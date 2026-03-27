# Net Art Corpus

This directory contains an aggregated corpus built from `data/sources/*/artworks.json`.

It does not replace source-specific data. It is a derived working layer for:

- large-scale deduplicated net art discovery
- extinction matching
- dependency inference
- queueing records for research and verification

## Files

- `netart-corpus.json`
  Merged corpus records with provenance from one or more sources.

- `extinction-matching-queue.json`
  Prioritized queue for extinction analysis. This is the practical working list for matching artworks against extinct dependencies and known extinction events.

- `source-stats.json`
  Simple counts and summary metrics for the source datasets used to build the corpus.

## Build

Run:

```bash
python scripts/build-netart-corpus.py
```

## Merge strategy

Records are merged conservatively:

- first by normalized artwork URL when available
- otherwise by normalized `title + artist + year`
- otherwise by normalized `title + artist`
- otherwise by normalized title only

This is deliberately imperfect. The goal is to create a large working corpus quickly, then improve it through later normalization.

## Extinction analysis fields

Each corpus record includes an `extinction_analysis` object intended for future enrichment:

- `status`
- `dependency_candidates`
- `extinction_event_candidates`
- `evidence_notes`
- `matched_event_ids`

The initial queue is seeded with heuristic evidence flags such as:

- `obsolete-runtime-tagged`
- `source-marked-dead`
- `source-marked-degraded`
- `archive-copy-known`
- `http-only-url`
- `historically-fragile-host`

## Scope

This corpus is meant to optimize for finding extinct or endangered net art, not for producing a pristine art-historical catalog on the first pass.
