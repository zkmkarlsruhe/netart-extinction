---
title: "Firefox removes <blink> tag — last browser support ends"
date: "2013-08-06"
dependency: "HTML <blink> element"
event_type: "browser-change"
severity: "minor"
summary: "Firefox 23 removed support for the <blink> HTML element, the last browser to do so. Invented by Netscape, <blink> was an iconic element of 1990s web aesthetics used deliberately by net artists — now impossible to render natively."
links:
  - url: "https://en.wikipedia.org/wiki/Blink_element"
    label: "Wikipedia: Blink element"
  - url: "https://www.fastcompany.com/3015408/saying-goodbye-to-the-html-tag"
    label: "Fast Company: Saying Goodbye to the HTML Blink Tag"
fixes:
  - type: workaround
    description: "The blinking effect can be recreated with CSS animations (@keyframes), but the semantic meaning of the <blink> tag — its cultural weight as a symbol of early web aesthetics — cannot be replicated."
  - type: none
    description: "No modern browser renders <blink>. Period-accurate display of 1990s web pages requires browser emulation."
---

Firefox 23 (August 6, 2013) removed support for the `<blink>` HTML element. Internet Explorer and WebKit/Chrome never supported it. Firefox was the last holdout, inheriting support from Netscape's Gecko engine.

## What changed

The `<blink>` tag was invented at Netscape (legend attributes it to Lou Montulli after a bar conversation in 1994). While widely derided as annoying, it became an iconic element of 1990s web culture. Net artists used it deliberately — as part of the raw, anti-design aesthetic of early web art, as ironic commentary on web conventions, or simply because it was there and it moved.

Its removal means period-accurate rendering of many 1990s web pages is now impossible in modern browsers. The companion tag `<marquee>` (Microsoft's counterpart, scrolling text horizontally) still partially works in modern browsers for compatibility reasons, but is also deprecated.

## Notes

The `<blink>` tag carries cultural weight beyond its visual effect. It symbolizes an era when the web was weird, personal, and unpolished — before web design became professionalized. CSS animations can recreate the visual effect, but not the cultural context of using the actual tag.
