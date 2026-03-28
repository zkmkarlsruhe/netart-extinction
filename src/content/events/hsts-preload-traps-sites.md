---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/HTTP_Strict_Transport_Security"
title: "HSTS preload list traps sites that lose HTTPS capability"
date: "2017"
dependency: "HTTP Strict Transport Security preload lists"
event_type: "protocol-change"
severity: "minor"
summary: "Sites added to browser HSTS preload lists became permanently locked into HTTPS; if their certificates later expired or were revoked, browsers refused all access — with no bypass option — creating an irreversible accessibility trap."
links:
  - url: "https://hstspreload.org/"
    label: "HSTS Preload List submission site"
  - url: "https://www.troyhunt.com/understanding-http-strict-transport/"
    label: "Troy Hunt: Understanding HTTP Strict Transport Security"
  - url: "https://chromium.googlesource.com/chromium/src/+/refs/heads/main/net/http/transport_security_state_static.json"
    label: "Chromium HSTS preload list (source)"
fixes:
  - type: workaround
    description: "Site operators can request removal from the HSTS preload list, but the process takes months to propagate through browser release cycles."
  - type: none
    description: "If the domain operator is unreachable or the domain has changed hands, the site may be permanently inaccessible in browsers that have it preloaded."
---

## What changed

HTTP Strict Transport Security (HSTS) allows websites to instruct browsers to always connect via HTTPS. The HSTS preload list, maintained by the Chromium project and adopted by Firefox, Safari, and Edge, goes further: sites on the list are hardcoded into the browser itself, meaning the browser will never attempt an HTTP connection to those domains, even on the first visit.

Getting onto the preload list is relatively easy — a site operator submits their domain and adds the appropriate HSTS header with the `preload` directive. Getting removed is slow: it requires a request to hstspreload.org, acceptance by the Chromium team, and then propagation through browser release cycles, which can take 6 to 12 months or longer.

This creates a trap. If a site is on the preload list and its TLS certificate expires, is revoked, or the site loses HTTPS capability for any reason, browsers will refuse to load the site entirely. Unlike regular HTTPS errors where browsers show a warning with a clickthrough option, HSTS-enforced failures are absolute — there is no "proceed anyway" button. The site is simply unreachable.

Several scenarios make this particularly dangerous for creative and artistic projects: domain ownership changes (the new owner may not configure HTTPS), hosting migrations where HTTPS is not re-enabled, certificate authority distrust events (like the Symantec distrust) where the site operator does not replace certificates, and expired Let's Encrypt certificates on unmaintained sites.

## Notes

The HSTS preload list is a one-way door that is easy to enter and hard to exit. For long-lived creative projects, being on the preload list means that any future lapse in HTTPS maintenance — even decades later — will make the site completely inaccessible rather than merely insecure. This is a subtle but permanent ratchet toward extinction for unmaintained web art.
