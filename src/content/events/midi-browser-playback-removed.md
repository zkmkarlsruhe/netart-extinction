---
ai_generated: true
title: "MIDI file playback removed from major browsers"
date: "2020"
dependency: "MIDI (.mid/.midi) browser-native playback"
event_type: "format-obsolescence"
severity: "major"
summary: "Browsers progressively dropped built-in MIDI file playback — Chrome removed its software synthesizer, Firefox never shipped reliable support, and the Web MIDI API that replaced it only handles real-time device I/O, not .mid file rendering — leaving thousands of MIDI-based web artworks and early net music projects silent."
links:
  - url: "https://en.wikipedia.org/wiki/MIDI#Web"
    label: "Wikipedia: MIDI on the web"
  - url: "https://developer.mozilla.org/en-US/docs/Web/API/Web_MIDI_API"
    label: "MDN: Web MIDI API (device I/O only, not file playback)"
  - url: "https://www.w3.org/TR/webmidi/"
    label: "W3C Web MIDI API specification"
fixes:
  - type: workaround
    description: "JavaScript libraries like MIDI.js and Tone.js can parse .mid files and synthesize audio in the browser via WebAudio, but the sound depends entirely on the chosen soundfont — the original GM/GS/XG synthesizer timbres are not preserved."
  - type: migration
    description: "MIDI files can be rendered to audio offline using period-appropriate synthesizers (e.g., a Roland SC-55 or Sound Canvas VA), but this destroys the interactive and generative qualities of MIDI-based artworks."
---

## What changed

In the early web era (roughly 1995–2005), browsers could play MIDI files natively. The `<embed>` and `<bgsound>` tags allowed authors to add MIDI music to pages, and the browser's built-in software synthesizer (or the operating system's General MIDI synth, such as the Microsoft GS Wavetable Synth on Windows or QuickTime's music synthesizer on Mac) would render the file in real time. MIDI was everywhere on personal homepages, fan sites, and early net art — it was the only music format small enough for dial-up connections.

Browser vendors removed MIDI support gradually and without formal announcement. Chrome dropped its built-in MIDI synthesizer around 2012–2013. Firefox never implemented reliable MIDI file playback beyond early experimental support. Safari's MIDI rendering, inherited from QuickTime, disappeared when QuickTime was deprecated. By 2020, no major browser could open a .mid file and produce sound without third-party JavaScript.

The W3C Web MIDI API (first shipped in Chrome 43, 2015) is not a replacement: it provides low-level access to hardware MIDI devices for real-time input/output, but has no facility for loading, parsing, or rendering Standard MIDI Files. An artist who embedded a .mid file in a webpage in 1998 cannot fix the silence by adopting the Web MIDI API.

The loss is compounded by the fact that MIDI playback was always synthesizer-dependent. Even when MIDI files survive, the specific sound the artist heard — determined by the GM-compatible synthesizer installed on their machine — is lost. A MIDI file rendered on a Yamaha MU80 sounds fundamentally different from the same file on a Sound Blaster AWE32 or a browser's built-in synth. The format's meaning was always entangled with its playback context.

Artists working with MIDI on the web included those creating generative compositions, interactive soundtracks that changed with user input, and deliberate explorations of the lo-fi MIDI aesthetic. The complete disappearance of browser MIDI playback silenced these works without warning or migration path.
