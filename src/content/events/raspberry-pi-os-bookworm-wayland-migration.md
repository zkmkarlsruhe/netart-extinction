---
ai_generated: true
title: "Raspberry Pi OS Bookworm switches to Wayland, breaking museum and art display software"
date: "2023-10-11"
dependency: "Raspberry Pi OS (X11 display server)"
event_type: "os-deprecation"
severity: "major"
summary: "Raspberry Pi OS Bookworm, released October 11, 2023, replaced X11 with Wayland as the default display server, breaking Pi Presents and other multimedia display tools widely used in museum installations and art kiosks."
links:
  - url: "https://www.raspberrypi.com/news/bookworm-the-new-version-of-raspberry-pi-os/"
    label: "Raspberry Pi: Bookworm — the new version of Raspberry Pi OS"
  - url: "https://pipresents.wordpress.com/news/"
    label: "Pi Presents news: Bookworm compatibility breaking changes"
  - url: "https://forums.raspberrypi.com/viewtopic.php?t=368337"
    label: "Raspberry Pi Forums: omxplayer under Bookworm"
  - url: "https://www.omglinux.com/raspberry-pi-os-bookworm/"
    label: "OMG! Linux: Raspberry Pi OS Now Uses Wayland & PipeWire"
fixes:
  - type: workaround
    description: "Operators can switch Bookworm back to X11 via raspi-config, but this is unsupported and may not be available in future releases."
  - type: rebuild
    description: "Pi Presents was rewritten as pipresents-gtk to support Wayland and the Raspberry Pi 5, but the rewrite introduced new bugs including video playback crashes."
  - type: workaround
    description: "Installations can remain on Bullseye Legacy images indefinitely, but these receive no security updates and are incompatible with the Raspberry Pi 5."
---

On October 11, 2023, Raspberry Pi OS Bookworm was released, based on Debian 12. The update replaced X11 with the Wayland display server (using the Wayfire compositor) as the default on Raspberry Pi 4 and 5 models, replaced DHCPD with NetworkManager, and moved PulseAudio to PipeWire.

## What changed

Raspberry Pi single-board computers have become the dominant platform for low-cost art installations, museum kiosks, digital signage, and interactive exhibits. Their affordability, small form factor, and Linux foundation made them the default choice for cultural institutions running multimedia displays. The Bookworm update broke this ecosystem in multiple ways.

Pi Presents — a multimedia toolkit specifically designed for museums, visitor centres, and gallery installations — was immediately broken by the Wayland migration. Pi Presents had been built on X11-specific display primitives and the omxplayer video player, which was deprecated and removed from Raspberry Pi OS repositories starting with Bullseye and completely unavailable on Bookworm. The developer was forced into a major rewrite (pipresents-gtk), which as of 2024 remained in beta with known video playback stability issues.

The omxplayer removal was particularly damaging. Many art installations used omxplayer for its ability to play video with hardware acceleration and precise control over looping, layering, and synchronization — capabilities that its replacement (VLC or mpv via GStreamer) did not replicate identically. Custom scripts written by artists and exhibit designers that called omxplayer directly stopped working entirely.

Raspberry Pi's own documentation acknowledged the severity of the changes: they explicitly stated that upgrading a Bullseye installation to Bookworm in-place was not supported and would "almost certainly end up with a non-booting desktop and data loss." For institutions running dozens of Pis in permanent installations, this meant the choice was to stay on an unsupported OS or rebuild every display from scratch.

## Notes

The Raspberry Pi ecosystem's fragility as an art platform stems from its consumer orientation. Updates are designed for hobbyists who reflash SD cards regularly, not for installations that need to run unattended for years. There is no long-term support channel for Raspberry Pi OS, and the Bullseye-to-Bookworm transition demonstrated that breaking changes to display, audio, and network subsystems can arrive simultaneously with no migration path.
