---
ai_generated: true
title: "SoundCloud API access reset and revocation of inactive apps"
date: "2023-06-02"
dependency: "SoundCloud API"
event_type: "terms-of-service"
severity: "major"
summary: "SoundCloud announced it would revoke API access for inactive apps (June 2, 2023), a policy shift that can break unattended installations and artworks that rely on SoundCloud API playback."
links:
  - url: "https://developers.soundcloud.com/blog/an-empty-blogpost/"
    label: "SoundCloud developer blog: changes for inactive apps"
affected_artworks:
  - artwork: singing-bridges
    severity: major
    status: degraded
    note: "Publishes audio via SoundCloud links/streams. If playback depends on app/API permissions, audio access can degrade."
fixes:
  - type: workaround
    description: "Prefer embeds over API where possible; keep embed code updated."
  - type: workaround
    description: "Ensure the app remains 'active' (maintenance pings, ownership, contact emails)."
  - type: archive
    description: "Preserve audio masters and self-host a fallback; store checksums and stable identifiers."
---

SoundCloud initiated an API access "reset," revoking some inactive apps and indicating a redesign of the API program. Works using API keys or "Enable app playback" patterns can fail without warning if their app is deemed inactive.

## Notes

Sound platforms are both technical and contractual dependencies; conservation should treat "account stewardship" as a material requirement.
