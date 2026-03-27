---
ai_generated: true
title: "Deutsche Telekom completes ISDN/PSTN switch-off in Germany"
date: "2020-01"
dependency: "ISDN telecommunications network (Germany)"
event_type: "network-shutdown"
severity: "major"
summary: "Deutsche Telekom migrated 25 million customers from ISDN/PSTN to All-IP between 2014 and early 2020, dismantling the circuit-switched network infrastructure that had enabled pioneering telematic art performances and real-time audiovisual installations since the early 1990s."
links:
  - url: "https://www.telekom.com/en/company/details/five-facts-about-the-ip-migration-596110"
    label: "Deutsche Telekom: Five facts about the IP migration"
  - url: "https://www.orange-business.com/en/magazine/dealing-with-the-great-isdn-switch-off"
    label: "Orange Business: Dealing with the great ISDN switch off"
  - url: "https://en.wikipedia.org/wiki/Telematic_art"
    label: "Wikipedia: Telematic art"
fixes:
  - type: migration
    description: "Telematic performance works that relied on ISDN's guaranteed-bandwidth circuit-switched connections must be redesigned for IP networks, which introduce variable latency and packet loss — fundamentally altering the real-time synchronization these works depended on."
  - type: none
    description: "The specific network conditions of ISDN — fixed 64/128 kbps channels with deterministic latency — cannot be reproduced on IP infrastructure. Works designed around these exact parameters can only be approximated, not faithfully re-performed."
---

Deutsche Telekom announced in 2014 its intention to migrate Germany's entire telecommunications infrastructure from ISDN and PSTN to All-IP by the end of 2018. The migration reached 86% by that deadline, with CEO Tim Hoettges declaring the process "formally accomplished" in early 2020 after 25 million customers — 99% of the base — had been switched.

## What changed

ISDN (Integrated Services Digital Network) provided dedicated circuit-switched digital channels with guaranteed bandwidth and deterministic latency. These properties made it the backbone of telematic art in the 1990s and 2000s — a genre of performance and installation art that connected remote spaces in real time.

Paul Sermon's "Telematic Dreaming" (1992) used ISDN video conferencing to create shared virtual beds between remote galleries. Between 1995 and 1998, a series of ISDN-connected concerts linked the Sonar Festival in Barcelona with Les Virtualistes in Paris, the HERE arts center in New York with Paris, the Musique Action festival in eastern France with Melbourne, and the Cyberia Internet cafe in Tokyo with the Web Bar in Paris. Maurice Benayoun's "Tunnel Sous l'Atlantique" (1995) at the Centre Pompidou used ISDN to create a virtual tunnel between Paris and Montreal.

These works were designed for ISDN's specific technical characteristics: fixed 64 kbps or 128 kbps channels that provided consistent, low-latency connections. The deterministic nature of circuit-switching — where a dedicated path is established for the duration of a connection — was not a limitation but a creative parameter. When ISDN infrastructure was dismantled, the network conditions these works were built around ceased to exist.

## Notes

Germany's ISDN switch-off was part of a global trend. France completed its migration by 2019, Japan and Australia phased out ISDN in the same period, and the UK's BT has extended its PSTN shutdown deadline to January 2027. Each shutdown removes another piece of the infrastructure that telematic art was created for. While IP networks can transmit the same data, they cannot replicate the deterministic timing relationships that were integral to how these works functioned and were experienced.
