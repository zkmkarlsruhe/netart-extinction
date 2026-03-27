---
ai_generated: true
title: "Gopher protocol support removed from major browsers"
date: "2010-01"
end_date: "2011-03"
dependency: "Gopher protocol support in web browsers"
event_type: "protocol-change"
severity: "major"
summary: "Firefox 4.0 (released March 2011) dropped built-in Gopher protocol support, completing a process that had already seen Internet Explorer disable Gopher in 2002 and Chrome never implement it — making Gopherspace unreachable from standard browsers and cutting off text-based art and literature hosted on Gopher servers."
links:
  - url: "https://bugzilla.mozilla.org/show_bug.cgi?id=388195"
    label: "Mozilla Bugzilla: Remove Gopher protocol support for Firefox"
  - url: "https://gopher.floodgap.com/overbite/relevance.html"
    label: "Overbite Project: Why still use Gopher?"
  - url: "https://en.wikipedia.org/wiki/Gopher_(protocol)"
    label: "Wikipedia: Gopher protocol"
fixes:
  - type: workaround
    description: "Browser extensions like OverbiteFF (Firefox) and Burrow (Chrome) restore Gopher access, but require manual installation and are intermittently maintained."
  - type: workaround
    description: "Web-based Gopher proxies (e.g., Floodgap's public proxy at gopher.floodgap.com) allow browsing Gopherspace through HTTP, though they flatten the native menu-driven experience."
  - type: none
    description: "Many university and institutional Gopher servers were decommissioned once browsers dropped support, taking their hosted content offline permanently."
---

Firefox 4.0, released in March 2011, was the last major browser to remove built-in Gopher protocol support. Internet Explorer had disabled Gopher in 2002 via a security patch, and Google Chrome never implemented it. After Firefox 4.0, visiting a gopher:// URL in any mainstream browser returned an error.

## What changed

Gopher, developed at the University of Minnesota in 1991, was the dominant hypertext protocol before the World Wide Web overtook it in the mid-1990s. At its peak, Gopherspace hosted thousands of servers at universities, libraries, and research institutions. A distinct culture of text-based publishing flourished there: structured document collections, literary archives, "phlogs" (Gopher-native blogs), and text art that exploited the protocol's hierarchical menu system.

When browsers dropped native support, the practical audience for Gopherspace collapsed. Server administrators at universities and institutions, already under pressure to consolidate infrastructure, lost the last justification for maintaining Gopher services. Servers that had quietly persisted for over a decade were decommissioned, taking their content with them. Unlike the web, Gopher content was rarely crawled by major search engines or captured by the Wayback Machine, so much of what disappeared left no trace.

Creative works that existed only on Gopher — text art collections, experimental hypertext literature, structured poetry projects that used Gopher's menu hierarchy as a navigational form — became accessible only through dedicated clients or proxy services that most users will never discover.

## Notes

Gopherspace has experienced a small revival since the mid-2010s, driven by interest in the "small web" and lightweight protocols. The Gemini protocol (launched 2019) draws directly on Gopher's design philosophy. However, the historical Gopherspace content from the 1990s and early 2000s — the material that was lost when institutional servers were shut down — remains largely unrecoverable. Floodgap's Veronica-2 search engine indexes surviving Gopher servers but cannot retrieve what no longer exists.
