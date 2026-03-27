---
ai_generated: true
title: "Browsers require HTTPS for geolocation, camera, and audio APIs"
date: "2016-04"
end_date: "2017-08"
dependency: "Powerful web APIs on HTTP pages"
event_type: "browser-change"
severity: "major"
summary: "Starting with Chrome 50 (April 2016), browsers restricted geolocation, camera/microphone access, Web Audio, and other powerful APIs to HTTPS-only 'secure contexts' — breaking location-aware art, webcam pieces, and audio works hosted on HTTP."
links:
  - url: "https://developer.chrome.com/blog/geolocation-on-secure-contexts-only"
    label: "Chrome: Geolocation on secure contexts only"
  - url: "https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts/features_restricted_to_secure_contexts"
    label: "MDN: Features restricted to secure contexts"
affected_artworks:
  - artwork: "singing-bridges"
    severity: major
    status: degraded
    note: "If hosted on HTTP, audio playback via Web Audio API would be blocked in modern browsers."
  - artwork: "soundboxes"
    severity: major
    status: degraded
    note: "Audio-interactive work. Web Audio API restrictions on HTTP would prevent functionality."
fixes:
  - type: migration
    description: "Migrate hosting to HTTPS. Free certificates are available from Let's Encrypt, but this requires server access and active maintenance."
  - type: none
    description: "For archived or abandoned art on HTTP servers, there is no fix without someone actively maintaining the hosting."
---

Starting with Chrome 50 (April 2016), the Geolocation API was restricted to HTTPS pages only. Firefox 55 (August 2017) followed. Subsequently, getUserMedia (camera/microphone), Web Audio API contexts, Service Workers, Web Bluetooth, Web MIDI, Push API, and the Payment Request API were all restricted to "secure contexts."

## What changed

Any web page served over HTTP lost access to the browser's most interactive capabilities: location sensing, camera and microphone input, advanced audio processing, push notifications, and device APIs. The APIs still exist but silently fail or throw errors on HTTP pages.

This disproportionately affects net art because many artworks are hosted on personal domains, university servers, or archived sites that serve over plain HTTP. Location-aware art, webcam-based interactive pieces, and audio works that relied on these APIs stopped functioning unless actively migrated to HTTPS hosting.

## Notes

Free HTTPS certificates (Let's Encrypt, launched 2016) made the technical migration straightforward — but it still requires someone with server access and motivation. For abandoned art on unmaintained servers, there is no one to perform the migration. The art silently degrades: it loads, it looks normal, but its interactive capabilities are gone.
