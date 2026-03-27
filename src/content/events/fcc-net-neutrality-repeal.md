---
ai_generated: true
title: "FCC repeals net neutrality rules"
date: "2017-12-14"
dependency: "Net neutrality protections (Open Internet Order 2015)"
event_type: "protocol-change"
severity: "minor"
summary: "The FCC voted to repeal net neutrality rules on December 14, 2017, enabling ISPs to throttle and prioritize traffic — researchers subsequently documented systematic throttling of video streaming services, degrading conditions for bandwidth-intensive net art, live-streamed performances, and independent video distribution."
links:
  - url: "https://www.npr.org/sections/thetwo-way/2017/12/14/570526390/fcc-repeals-net-neutrality-rules-for-internet-providers"
    label: "NPR: FCC Repeals Net Neutrality Rules"
  - url: "https://publicknowledge.org/two-years-later-broadband-providers-are-still-taking-advantage-of-an-internet-without-net-neutrality-protections/"
    label: "Public Knowledge: Two Years Later, Broadband Providers Still Taking Advantage"
  - url: "https://switchboard.live/blog/net-neutrality-live-streaming"
    label: "Switchboard: Impact of Net Neutrality Repeal on Live Streaming"
fixes:
  - type: workaround
    description: "Artists and small platforms can use CDNs and adaptive bitrate streaming to partially mitigate throttling, but this adds cost and complexity that disproportionately burdens independent creators."
  - type: none
    description: "The structural asymmetry — large platforms can negotiate peering agreements and zero-rating deals that independent art servers cannot — is an ongoing condition with no technical fix."
---

On December 14, 2017, the FCC voted 3-2 to repeal the Open Internet Order of 2015, eliminating rules that had prohibited internet service providers from blocking, throttling, or creating paid fast lanes for internet traffic. The repeal took effect on June 11, 2018.

## What changed

The repeal did not cause an immediate, visible catastrophe for online art. Its damage was structural and cumulative, creating a tiered internet where bandwidth-intensive work by independent artists faced systematically worse delivery conditions than content from large commercial platforms.

Researchers from Northeastern University and the University of Massachusetts Amherst documented the consequences empirically: from early 2018 to early 2019, AT&T throttled Netflix 70% of the time and YouTube 74% of the time — but not Amazon Prime Video. T-Mobile throttled Amazon Prime Video in 51% of tests but left Skype and Vimeo untouched. These were not transparent network management policies but selective, undisclosed degradation of specific services.

For net art and online creative work, the implications were clear. An artist streaming a live performance on an independent server, or hosting high-resolution video art on a personal domain, was competing for bandwidth against platforms that could negotiate zero-rating deals and priority peering arrangements. AT&T exempted its own DirecTV Now streaming service from customers' data caps, meaning a video artwork hosted on any other platform was effectively more expensive to watch on mobile.

The repeal created conditions that favored consolidation: artists migrated to major platforms (YouTube, Vimeo, Instagram) not because those platforms were better suited to their work, but because the work would actually reach audiences without buffering or data-cap penalties. This further concentrated creative distribution through a small number of corporate gatekeepers — platforms that impose their own content policies, algorithmic curation, and format constraints on the work they host.

## Notes

Net neutrality's impact on art is a slow-acting structural harm rather than a discrete extinction event. No single artwork died on December 14, 2017. But the repeal shifted the economics of online art distribution in ways that continue to push independent, bandwidth-intensive creative work toward platform dependency.
