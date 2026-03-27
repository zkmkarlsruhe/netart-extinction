Here’s a **clean system prompt / task spec** you can give to a coding agent.
No fluff, just what it needs to execute.

---

# Agent Instructions: Setup “Net Art Extinction Timeline”

## Goal

Create a **Git-based static website** for the project:

**Name:** Net Art Extinction Timeline
**Primary domain:** extinction.zkm.de
**Future domain:** netart-extinction.com

The site documents **dependency change events and their impact on artworks**.

---

## Tech Stack

* Framework: **Astro**
* Content: Markdown (MD) with frontmatter
* Repo: GitHub
* Deployment: static hosting (NGINX or GitHub Pages or similar)
* No database
* No CMS (for now)

---

## Core Requirements

### 1. Content structure

Create a content collection:

```
/src/content/events/
```

Each file = one event.

Filename format:

```
YYYY-MM-DD__slug.md
```

Example:

```
2023-02-09__twitter-api-change.md
```

---

### 2. Event template

All event files must follow this schema:

```md
---
title: string
date: YYYY-MM-DD

dependency: string
event_type: api_change | api_pricing | plugin_eol | browser_change | protocol_change | domain_loss | hosting_shutdown | platform_policy | other

summary: string

links:
  - string
---

## What changed

text

## Affected artworks

### Title — Artist (Year)
- url: string
- dependency usage: string
- failure: string
- severity: total | major | minor
- status: dead | degraded | restored | unknown

## Fix / workaround

### Title
- type: emulation | proxy | rewrite | mirror | none | unknown
- description: string
- link: string

## Notes

text
```

---

### 3. Validation

Use Astro content collections + schema validation:

* enforce required fields:

  * title
  * date
  * dependency
  * event_type
  * summary

* enforce enums:

  * event_type
  * severity
  * status
  * fix type

Reject invalid content at build time.

---

### 4. Pages

#### Homepage

* Title + short description
* Reverse chronological list of events
* Each item:

  * title
  * date
  * dependency
  * summary

---

#### Event page

Route:

```
/events/[slug]
```

Show:

* metadata (title, date, dependency, type)
* summary
* full content sections
* links

---

#### Timeline view (simple)

* grouped by year
* no complex visualization needed

---

### 5. Contribution flow

Add:

```
/CONTRIBUTING.md
```

Content:

* explain concept in 3–4 sentences
* explain file naming
* provide copy-paste template
* explain how to open PR

---

### 6. GitHub Issue Forms

Create:

```
.github/ISSUE_TEMPLATE/
```

#### Form 1: report_event.yml

Fields:

* title
* date
* dependency
* description
* affected artworks
* links
* fixes

#### Form 2: report_artwork.yml

Fields:

* artwork title
* artist
* event (optional)
* what broke
* severity
* status
* evidence
* workaround

Keep forms minimal.

---

### 7. Email submission

Add visible contact:

```
submit@extinction.zkm.de
```

Add page section:

“Submit by email”

Text:

* rough reports are welcome
* include:

  * what changed
  * when
  * what broke
  * links/evidence

---

### 8. Styling

Keep minimal:

* clean typography
* no heavy design system
* focus on readability
* light + dark mode optional

No animations required.

---

### 9. SEO / metadata

Set:

* site title: Net Art Extinction Timeline
* description: Tracking how dependency changes break digital artworks
* canonical URL: extinction.zkm.de

---

### 10. Deployment

* build static output
* deploy to:

  ```
  extinction.zkm.de
  ```
* ensure:

  * HTTPS
  * fast load
  * no server-side logic

---

## Non-Goals (do NOT implement)

* user accounts
* database
* artwork hosting
* API backend
* complex visualizations
* search (for now)

---

## Nice-to-have (optional)

* tag filtering (by dependency or event_type)
* simple JSON export of all events
* RSS feed

---

## Deliverables

* working Astro project
* example content (at least 2 events)
* deployed site
* GitHub repo with:

  * README
  * CONTRIBUTING
  * issue forms

---

## Guiding principle

> Document **dependency changes → impact on artworks → possible fixes**

Not:

* archive artworks
* build a museum system

---

If anything is unclear:

* prefer simplicity
* avoid overengineering
* prioritize content over features

