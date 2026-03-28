---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Code_signing"
title: "Expired code signing certificates break installed applications"
date: "2019-10-24"
dependency: "Code signing certificate timestamps"
event_type: "certificate-expiry"
severity: "minor"
summary: "An expired Symantec/VeriSign code signing intermediate certificate on October 24, 2019 caused Windows to flag previously trusted signed software as untrusted, breaking installers and legacy applications that lacked RFC 3161 timestamps."
links:
  - url: "https://knowledge.digicert.com/alerts/code-signing-issue-with-cross-signed-verisign-symantec-timestamp"
    label: "DigiCert: Code Signing Issue with Cross-Signed Timestamp Certificates"
  - url: "https://docs.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures"
    label: "Microsoft: Time Stamping Authenticode Signatures"
---

## What changed

On October 24, 2019, a VeriSign Class 3 Code Signing 2010 CA intermediate certificate expired. This certificate had been used as part of the Symantec (later DigiCert) code signing chain for years. When it expired, Windows systems began treating software signed through this chain as having invalid signatures — but only for executables that had not been counter-signed with an RFC 3161 timestamp.

Code signing with a proper timestamp is supposed to anchor the signature's validity to the moment it was made: even after the signing certificate expires, the timestamp proves the signature was created while the certificate was still valid. However, many developers — particularly small studios, independent artists distributing interactive works, and academic projects — signed their executables without timestamps, either through misconfigured build processes or simple oversight.

The result was that previously working installed applications suddenly triggered Windows SmartScreen warnings or outright execution blocks. Creative coding tools, interactive art installations distributed as Windows executables, and legacy software packages all became suspect overnight. For projects whose developers had moved on, there was no one to re-sign the binaries.

This failure mode is particularly insidious for digital preservation: a perfectly functional archived executable can become unlaunchable simply because time has passed and the certificate chain it was signed with has decayed. The binary itself is unchanged, but the trust infrastructure around it has expired.
