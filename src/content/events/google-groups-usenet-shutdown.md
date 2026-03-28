---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Google_Groups"
title: "Google Groups ends Usenet support, severing the largest public NNTP gateway"
date: "2024-02-22"
dependency: "Google Groups Usenet/NNTP gateway"
event_type: "network-shutdown"
severity: "major"
summary: "Google Groups ceased all new Usenet posting, subscription, and NNTP peering on February 22, 2024, cutting off the largest remaining free public gateway to Usenet newsgroups including communities like alt.ascii-art that had hosted text-based art since the early 1990s."
links:
  - url: "https://www.bleepingcomputer.com/news/google/google-groups-is-ending-support-for-usenet-to-combat-spam/"
    label: "BleepingComputer: Google Groups ending Usenet support"
  - url: "https://www.theregister.com/2023/12/18/google_ends_usenet_links/"
    label: "The Register: Google Groups ditches links to Usenet"
  - url: "https://mjtsai.com/blog/2023/12/20/google-groups-ending-support-for-usenet/"
    label: "Michael Tsai: Google Groups Ending Support for Usenet"
fixes:
  - type: archive
    description: "Google retained historical Usenet archives (dating back to 1981 via the former Deja News acquisition) for read-only viewing and search, though the long-term availability of this archive is not guaranteed."
  - type: workaround
    description: "Remaining Usenet access requires dedicated NNTP providers like Eternal September or commercial providers, raising the barrier to entry significantly."
---

On February 22, 2024, Google Groups stopped accepting new Usenet posts, disabled subscriptions to Usenet newsgroups, and shut down its NNTP server and peering connections. Google cited declining legitimate activity and rising spam as justification.

## What changed

Google Groups had been the last major free, publicly accessible gateway between the web and Usenet. For most casual users, it was the only way they ever encountered Usenet at all. Its removal severed the most accessible bridge to a network that had been foundational to digital culture since the 1980s.

Usenet newsgroups had been home to significant text-based art communities. The alt.ascii-art hierarchy, active since the early 1990s, was one of the longest-running collaborative digital art spaces in existence — a place where artists created, critiqued, and catalogued ASCII art across thousands of threads. Groups like alt.ascii-art, alt.ascii-art.animation, and rec.arts.ascii maintained FAQs, style guides, and community standards that constituted a living archive of text-based visual culture. Other creative newsgroups — alt.fan.warlord, rec.arts.poems, comp.music.midi — hosted decades of creative output and critical discussion.

While existing historical content remains searchable through Google Groups' web interface, the cessation of NNTP peering means Google's copy of these archives is now frozen. No new contributions can flow in, and the archives are entirely dependent on Google's continued willingness to host them. Earlier Usenet history already suffered a blow when Google redesigned Groups in 2013, breaking many deep links to archived posts.

## Notes

The shutdown of Google's NNTP gateway compounds earlier losses in the Usenet ecosystem: the closure of free NNTP providers Aioe.org and Albasani reduced the number of accessible entry points. For art communities that relied on Usenet's decentralized, persistent, threaded discussion model — a fundamentally different structure from web forums or social media — each lost gateway makes the remaining culture harder to reach and easier to forget.
