---
title: "Browsers restrict powerful APIs to HTTPS-only secure contexts"
date: "2016-04"
end_date: "2017-08"
dependency: "Geolocation, getUserMedia, Web Audio, and other browser APIs on HTTP"
event_type: "browser-change"
severity: "major"
summary: "Starting with Chrome 50 in April 2016, browsers began restricting 'powerful' APIs — geolocation, camera/microphone, audio context, notifications — to HTTPS pages only. Net art hosted on HTTP servers lost access to location, webcam, and audio APIs."
links:
  - url: "https://developer.chrome.com/blog/geolocation-on-secure-contexts-only"
    label: "Chrome Developers: Geolocation on Secure Contexts Only"
  - url: "https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Secure_Contexts/features_restricted_to_secure_contexts"
    label: "MDN: Features restricted to secure contexts"
fixes:
  - type: migration
    description: "Migrate hosting to HTTPS with a valid TLS certificate (free via Let's Encrypt). Requires active server access."
  - type: none
    description: "For archived or unmaintained art on HTTP servers, these APIs are permanently broken with no client-side workaround."
---

Starting with Chrome 50 (April 2016), browsers began requiring HTTPS ("secure context") for access to powerful web APIs. The Geolocation API was first. Firefox 55 (August 2017) followed. Subsequently, getUserMedia (camera/microphone), AudioContext, Notification API, Service Workers, Web Bluetooth, Web MIDI, and more were all restricted to secure contexts.

## What changed

Any net artwork hosted on an HTTP server that used geolocation, webcam input, microphone access, or the Web Audio API stopped functioning in modern browsers. The APIs simply return errors or are undefined on insecure pages.

This is particularly damaging because many historical net art sites are hosted on personal domains, university servers, or archived infrastructure that serves over HTTP. Adding HTTPS requires active server access and maintenance — exactly what abandoned art sites lack. Even works preserved by institutions may be served from HTTP archives.

## Notes

The fix is technically simple (add a TLS certificate, available free from Let's Encrypt), but requires someone with server access and motivation. For the class of art this most affects — experimental, small-scale, hosted on forgotten infrastructure — there is often no one.
