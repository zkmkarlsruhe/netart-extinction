# Net Art Extinction Coverage Research

Date: 2026-03-27
Scope: Research-only assessment of the current extinction-event corpus in this repo, focused on net art.
Constraint: No existing repo content was modified as part of this note.

## Framing

This assessment uses a stricter definition of "extinction event" for net art:

- Not every deprecation, version jump, or ecosystem migration counts.
- A strong extinction event is one where a web-native artistic form, runtime, host, distribution channel, feed layer, browser capability, or platform materially disappeared.
- "Flash blocked" counts.
- "JavaScript API v1 retired and old embeds stop functioning" can count.
- Ordinary library churn, minor version incompatibilities, and general maintenance burden usually do not.

## Current Corpus Snapshot

- Event files currently present: 116
- The corpus is broad, but that count overstates coverage of true extinction events because some entries are better described as degradation pressures, policy hardening, or ordinary software churn.

## High-Level Assessment

### Stronger coverage areas

- Browser plugin death and browser-embedded runtimes
  - Flash
  - Shockwave
  - Silverlight
  - NPAPI / Java plugin
  - QuickTime VR / QuickTime browser plugin
  - VRML browser plugins
  - Beatnik
  - Pulse 3D

- Platform shutdowns and hosted-net-culture disappearance
  - GeoCities
  - GeoCities Japan
  - Google+
  - Vine
  - Posterous
  - Yahoo Answers
  - Yahoo Groups content purge
  - PlayStation Home
  - Friendster / Imeem / Blip.tv / What.CD / Megaupload

- Some genuine network / protocol / infrastructure extinctions
  - FTP removed from browsers
  - Gopher removed from browsers
  - TLS 1.0 / 1.1 dropped
  - SHA-1 certificate rejection
  - Symantec / StartSSL / CNNIC trust collapses
  - 3G network shutdowns
  - US analog TV shutdown

### Coverage weaknesses

- Browser-era web platform removals are underrepresented.
- Feed / mashup / aggregation infrastructure is underrepresented.
- Hosted map / live-data net art dependencies are underrepresented.
- Some current entries are not strong extinction events under a net-art-specific definition.

## Net-Art-Specific Reading of Coverage

### Overall judgment

- The repo covers many famous plugin deaths and a fair number of platform shutdowns.
- It does not yet cover enough of the central net-art substrate events: feed systems, map layers, browser-hosted app models, and browser platform removals.
- The set is best described as broad but noisy, not cleanly canonical.

## Missing Events: Highest Priority

These are the missing events that best fit a strict net art extinction definition.

### 1. Yahoo Pipes shutdown

Why it matters:

- A major missing event.
- Yahoo Pipes was core infrastructure for mashup, feed-based, recombinatory, and automated web-native work.
- Its shutdown is much more central to net art than many existing SDK/library deprecations in the repo.

Timeline:

- Read-only on 2015-08-30
- Shutdown on 2015-09-30

Status of sourcing:

- I did not quickly find a live first-party Yahoo page during this pass.
- The event is well documented in secondary reporting.

Research links:

- https://www.ghacks.net/2015/06/05/yahoo-shuts-down-pipes-maps-and-other-services/
- https://www.infodocket.com/2015/06/05/time-to-say-goodbye-the-end-of-yahoo-pipes/

### 2. Google Reader shutdown

Why it matters:

- Important for RSS-driven and subscription/feed-based artworks.
- RSS syndication and reading environments were part of net art's distribution and reception ecology.

Timeline:

- Shutdown on 2013-07-01

Primary source:

- Google announced the retirement directly.

Research link:

- https://blog.google/company-news/inside-google/company-announcements/a-second-spring-of-cleaning/

### 3. Fusion Tables shutdown

Why it matters:

- Strong fit for net art that depends on hosted live datasets, map overlays, and browser-based data display.
- More defensible as a net-art extinction event than generic framework deprecations.

Timeline:

- Shutdown on 2019-12-03

Primary/official sources:

- Google sunset documentation for Apps Script and Maps-related dependencies.

Research links:

- https://developers.google.com/apps-script/guides/support/sunset
- https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap

### 4. Google Maps JavaScript API v2 retirement

Why it matters:

- Very strong fit for locative, cartographic, and embedded-map-based net art.
- Old embedded works stop working unless migrated.
- This is a hard retirement, not ordinary version churn.

Timeline:

- No longer available as of 2021-05-26

Primary source:

- Google's migration documentation explicitly says v2 is no longer available.

Research link:

- https://developers.google.com/maps/documentation/javascript/v2tov3

### 5. Application Cache removal

Why it matters:

- Real browser-platform extinction.
- Important for offline or self-contained website works.
- Better fit than many current entries that describe softer compatibility problems.

Timeline:

- Removal process began in Chrome 85 in 2020
- Fully removed by 2021-10-05

Primary/official sources:

- Chrome and web.dev documentation

Research links:

- https://developer.chrome.com/blog/chrome-85-deps-rems/
- https://web.dev/articles/appcache-removal

### 6. Native Client / PNaCl removal

Why it matters:

- Hard runtime extinction for browser-hosted compiled interactive work.
- Relevant where artworks depended on Native Client or Portable Native Client in the browser.

Timeline:

- PNaCl open-web deprecation announced for Q4 2019
- Broader support ended by 2021

Primary/official sources:

- Chrome deprecation and migration documentation

Research links:

- https://developer.chrome.com/docs/native-client/migration
- https://developer.chrome.com/deprecated

### 7. Chrome Apps end-of-life

Why it matters:

- Relevant for browser-packaged, kiosk-like, installational web works.
- Less central than Yahoo Pipes or Fusion Tables, but still stronger than many current library-migration entries.

Timeline:

- Deprecated outside ChromeOS first
- Final ChromeOS support ended in January 2025

Primary/official sources:

- Chrome Apps documentation and migration docs

Research links:

- https://developer.chrome.com/docs/apps/
- https://developer.chrome.com/docs/apps/migration

### 8. Web Components v0 / HTML Imports / Custom Elements v0 removal

Why it matters:

- This is the browser-platform event that matters more than "Polymer went into maintenance mode."
- Relevant where the work itself depends on that browser-era component model.
- Stronger event framing than a framework maintenance shift.

Timeline:

- Removal effectively crystallized in 2019

Primary/official source:

- Chrome's upgrade guidance around deprecated Web Components v0 technologies

Research link:

- https://developer.chrome.com/blog/web-components-time-to-upgrade/

## Existing Repo Entries That Look Weak for a Strict Net-Art Canon

These may still matter as preservation pressures, but they are weak candidates for the main extinction canon.

- `openframeworks-glm-migration`
- `threejs-geometry-removal`
- `python2-end-of-life`
- `processing-js-deprecated`
- `raspberry-pi-os-bookworm-wayland-migration`
- `max-msp-8-drops-32bit`
- `browser-form-rendering-drift`
- `fcc-net-neutrality-repeal`
- `domain-expiration-hosting-lapses`

Reasoning:

- These are mostly creative-coding ecosystem changes, OS/toolchain burden, or general preservation problems.
- They do not map cleanly to net art extinction in the same way as the death of a browser plugin, a feed platform, an embeddable map runtime, or a hosted platform shutdown.

## Existing Repo Entries That Look Borderline or Need Reframing

These are not necessarily wrong, but they may need stricter editorial framing.

### `polymer-deprecated-for-lit`

- Weak as currently framed.
- "Polymer maintenance mode" is not itself a net art extinction event.
- The stronger event is removal of Web Components v0 and HTML Imports support in browsers.

### `webvr-api-deprecated`

- Borderline but defensible.
- This is stronger if framed as the disappearance of first-generation browser VR runtime compatibility for unmaintained web experiences.
- Still less central to net art than Yahoo Pipes, Fusion Tables, or Maps API v2 retirement.

### `https-required-for-apis`

- Potentially defensible if tied to specific classes of HTTP-hosted net art that lost geolocation, camera, microphone, or audio functionality.
- Better if kept as one tightly framed secure-context event rather than duplicated.

### `secure-context-https-required`

- Appears to overlap with `https-required-for-apis`.
- Likely duplication.

### `processing-js-deprecated`

- Weak if framed only as "project archived."
- Stronger only if there is evidence of actual browser-hosted sketches ceasing to run at scale due to runtime assumptions or platform breakage.

### `threejs-geometry-removal`

- Too close to ordinary framework churn for the core canon.
- Relevant to preservation practice, but not a canonical extinction event in the same sense as Flash or GeoCities.

### `openframeworks-glm-migration`

- Primarily a toolkit migration problem for compiled digital art.
- Not net art in the strict sense.

### `browser-form-rendering-drift`

- Conceptually interesting and art-historically real.
- But not a discrete extinction event.
- Better treated as slow medium mutation than event extinction.

### `cross-origin-corb-tightening`

- Could matter for scraping/mashup art.
- But current framing is broad, diffuse, and more like policy hardening than a single extinction event.

### `popup-blocking-default`

- This is stronger than most browser-policy entries because it extinguished a recognizable formal vocabulary of popup-based net art.
- It is a legitimate net-art event even though it is browser-policy-driven.

### `autoplay-policies-block-sound`

- Borderline.
- Significant for some works, but weaker than hard runtime or platform death.

## Existing Repo Entries That Look Duplicative

### `crt-monitor-extinction` / `crt-monitor-obsolescence`

- Likely duplicate concept.

### `https-required-for-apis` / `secure-context-https-required`

- Clear overlap.

### `npapi-java-plugin-removal` / `java-7u51-applet-lockdown`

- The latter looks more like a precursor security ratchet.
- The former is the stronger extinction event.

## Coverage Summary by Category

### Canonical areas already reasonably covered

- Browser plugin extinction
- Hosted social/media/community platform shutdown
- Some browser protocol removals
- Some certificate trust-chain collapses

### Canonical areas still undercovered

- Feed infrastructure
- Mashup infrastructure
- Hosted map/data layers
- Browser-hosted application runtimes
- Browser platform removals distinct from ordinary framework churn

## Working Editorial Recommendation

If the project wants a cleaner and more defensible canon of net art extinction events:

1. Keep the hard shutdown/removal corpus.
2. Separate "extinction events" from "degradation pressures."
3. Add the missing high-priority net-art substrate events before adding more framework/version breakage.

## Proposed Prioritization for Future Additions

Top priority missing additions:

1. Yahoo Pipes shutdown
2. Google Reader shutdown
3. Fusion Tables shutdown
4. Google Maps JavaScript API v2 retirement
5. Application Cache removal
6. Native Client / PNaCl removal
7. Web Components v0 / HTML Imports removal
8. Chrome Apps end-of-life

## Short Conclusion

The current repo likely covers many of the most famous browser-plugin deaths, but it does not yet cover enough of the central net-art infrastructure extinctions.

The biggest gap is not "more libraries that changed API."
The biggest gap is the disappearance of feed systems, mashup layers, hosted map/data infrastructure, and browser-hosted web runtimes that net art actually depended on.
