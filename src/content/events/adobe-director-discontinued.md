---
title: "Adobe discontinues Director authoring tool"
date: "2017-02-01"
dependency: "Adobe Director / Lingo scripting"
event_type: "plugin-eol"
severity: "total"
summary: "Adobe ceased sales of Director on February 1, 2017 and ended support on March 14, killing the dominant authoring environment for interactive multimedia since the late 1980s. Existing .dir/.dxr source files became unopenable — no successor tool can edit them."
links:
  - url: "https://blog.adobe.com/en/publish/2017/01/27/the-future-of-adobe-contribute-director-and-shockwave"
    label: "Adobe: The Future of Director and Shockwave"
  - url: "https://en.wikipedia.org/wiki/Adobe_Director"
    label: "Wikipedia: Adobe Director"
affected_artworks:
  - artwork: carrier
    severity: total
    status: dead
    note: "Director/Shockwave project. Even if the Shockwave Player somehow ran, the source .dir files can no longer be edited to fix or update the work."
  - artwork: new-lexia
    severity: total
    status: dead
    note: "Director/Shockwave interactive. Source files unopenable without legacy Director installation."
  - artwork: soundboxes
    severity: total
    status: dead
    note: "Director/Shockwave audio piece. Authoring tool death means no path to updating the work."
fixes:
  - type: archive
    description: "The Flashpoint Archive has preserved 25,000+ Shockwave titles. The open-source ProjectorRays decompiler can reconstruct Lingo code from compiled files."
  - type: none
    description: "No successor authoring environment exists. Director's Lingo scripting language and score-based timeline have no equivalent in any current tool."
---

Adobe announced the discontinuation of Director on January 27, 2017. Sales ceased February 1, 2017, and all updates and support ended March 14, 2017. The final version was Director 12, released February 11, 2013.

## What changed

Director (originally MacroMind VideoWorks, 1985) was the dominant authoring environment for interactive multimedia for nearly three decades. It used the Lingo scripting language and a score-based timeline to create interactive CD-ROM art, museum kiosks, web-based Shockwave content, and standalone installations. Its discontinuation is distinct from the Shockwave Player EOL (April 2019, documented separately): Director's death killed the ability to create or edit content, while Shockwave's death killed the ability to view it.

The .dir (source) and .dxr (protected) file formats are proprietary and can only be opened in Director itself. With no supported version available, existing source files are effectively locked — even if an artist wanted to update a work for modern platforms, they cannot open their own source files in any current tool.

## Notes

The open-source ProjectorRays decompiler can reconstruct Lingo code from compiled Director files, offering a partial preservation path. But the score-based timeline, cast members, and behavioral scripting model have no equivalent in any modern authoring environment. Director wasn't just a tool — it was a way of thinking about interactive media that has no successor.
