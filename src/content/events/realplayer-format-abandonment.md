---
ai_generated: true
title: "RealAudio/RealVideo format abandoned, last broadcaster drops support"
date: "2011-03"
dependency: "RealPlayer / RealAudio / RealVideo streaming"
event_type: "plugin-eol"
severity: "major"
summary: "BBC World Service dropped RealAudio in March 2011, the last major broadcaster to use the format. RealNetworks had already pivoted away from streaming, and the browser plugin died with NPAPI removal. Early streaming net art and net radio projects using .ra/.rm/.ram formats became inaccessible."
links:
  - url: "https://en.wikipedia.org/wiki/RealPlayer"
    label: "Wikipedia: RealPlayer"
  - url: "https://en.wikipedia.org/wiki/RealAudio"
    label: "Wikipedia: RealAudio"
fixes:
  - type: emulation
    description: "RealMedia files can still be decoded by some desktop media players (VLC), but browser-embedded playback via the RealPlayer plugin is impossible."
  - type: none
    description: "The streaming server infrastructure (RealServer/Helix) is gone. Live-streamed works that depended on the RealMedia streaming protocol cannot be replayed."
affected_artworks:
  - artwork: "airworld"
    severity: total
    status: dead
  - artwork: "anti-capitalist-operating-system"
    severity: total
    status: dead
  - artwork: "being-human"
    severity: total
    status: dead
  - artwork: "bindigirl"
    severity: total
    status: dead
  - artwork: "bodies-incorporated"
    severity: total
    status: dead
  - artwork: "document-9-1-1"
    severity: total
    status: dead
  - artwork: "frustration-machine"
    severity: total
    status: dead
  - artwork: "gl-v"
    severity: total
    status: dead
  - artwork: "home-transfer"
    severity: total
    status: dead
  - artwork: "i-want-to-share-you-what-are-you-doing-to-me"
    severity: total
    status: dead
  - artwork: "in-conversation"
    severity: total
    status: dead
  - artwork: "jessambola"
    severity: total
    status: dead
  - artwork: "la-fabrica"
    severity: total
    status: dead
  - artwork: "learning-to-love-you-more"
    severity: total
    status: dead
  - artwork: "metronome"
    severity: total
    status: dead
  - artwork: "multiple-dwelling"
    severity: total
    status: dead
  - artwork: "n3xt"
    severity: total
    status: dead
  - artwork: "nonsense"
    severity: total
    status: dead
  - artwork: "one-night-in-greenwich-village"
    severity: total
    status: dead
  - artwork: "oppera-teorettikka-internettikka"
    severity: total
    status: dead
  - artwork: "pan-o-matic-website-number-0001"
    severity: total
    status: dead
  - artwork: "photomontage"
    severity: total
    status: dead
  - artwork: "pliages-et-d"
    severity: total
    status: dead
  - artwork: "plotfracture"
    severity: total
    status: dead
  - artwork: "polar-inertia"
    severity: total
    status: dead
  - artwork: "singing-bridges"
    severity: total
    status: dead
  - artwork: "the-act"
    severity: total
    status: dead
  - artwork: "the-sour-thunder"
    severity: total
    status: dead
  - artwork: "thebigear-an-imaginary-soundscape"
    severity: total
    status: dead
  - artwork: "turnbaby"
    severity: total
    status: dead
  - artwork: "us-department-of-art-technology"
    severity: total
    status: dead
  - artwork: "violence"
    severity: total
    status: dead
  - artwork: "what-was-he-thinking-about-berlin-praha-ljubljana-skopje"
    severity: total
    status: dead
  - artwork: "when-going-from-to"
    severity: total
    status: dead
  - artwork: "wnvirus-com"
    severity: total
    status: dead
---

RealAudio (launched April 1995) was the first widely adopted streaming audio format on the web. RealVideo followed in 1997. By the early 2000s, RealPlayer was installed on hundreds of millions of computers. But the company's aggressive installation practices and bloated software drove users away, and the format was progressively displaced — first by Flash video, then by HTML5 audio/video.

## What changed

BBC World Service discontinued RealAudio in March 2011, the last major broadcaster to drop the format. The browser plugin was killed by NPAPI removal in 2015–2017. The proprietary .ra/.rm/.ram formats are now effectively orphaned — while VLC and some desktop players can still decode the files, browser-embedded playback is impossible, and the streaming server infrastructure no longer exists.

Sound artists and net radio projects used RealAudio streaming for broadcast art. Radioqualia (founded 1998) and other early net radio initiatives built their distribution on RealAudio streams. RealFlash — a hybrid format synchronizing Flash animation with RealAudio streams — was an early rich-media web format that has no modern equivalent.

## Notes

RealMedia's death was gradual rather than a single kill date. Unlike Flash (which had a definitive EOL), RealNetworks simply stopped being relevant. The company still exists but pivoted entirely away from the streaming format it created.
