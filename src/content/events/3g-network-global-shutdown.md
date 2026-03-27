---
ai_generated: true
title: "Global 3G network shutdowns disconnect IoT and connected artworks"
date: "2022-02-22"
dependency: "2G/3G cellular network infrastructure"
event_type: "network-shutdown"
severity: "major"
summary: "Mobile carriers worldwide shut down 2G and 3G networks between 2019 and 2025, disconnecting millions of IoT devices — including connected art installations and sensor-based artworks relying on legacy cellular modules."
links:
  - url: "https://www.iot-now.com/2022/10/17/124627-the-termination-of-2g-and-3g-mobile-networks-and-the-effect-on-iot/"
    label: "IoT Now: The termination of 2G and 3G networks and the effect on IoT"
  - url: "https://www.gsma.com/connectivity-for-good/2g-3g-switch-off/"
    label: "GSMA: 2G/3G switch-off tracker"
fixes:
  - type: migration
    description: "Replace 3G cellular modules with 4G LTE or 5G equivalents. Requires physical access and often a complete electronics redesign."
  - type: none
    description: "Permanently installed or remote artworks with embedded 3G modules and no upgrade path lose connectivity entirely."
---

## What changed

Starting in the late 2010s, mobile carriers worldwide began shutting down their 2G and 3G networks to repurpose spectrum for 4G LTE and 5G. The shutdowns rolled across continents:

- **Japan**: NTT Docomo shut down FOMA (3G) in March 2026, KDDI ended 3G in March 2022, SoftBank in January 2024
- **Australia**: Telstra shut down 3G in June 2024, after earlier closing 2G in 2016
- **United States**: AT&T (February 2022), T-Mobile (July 2022), Verizon (December 2022)
- **South Korea**: SK Telecom, KT, and LG U+ shut down 2G between 2020-2021
- **Europe**: Swisscom (end of 3G in 2025), Vodafone UK (2G/3G shutdown planned 2025), Deutsche Telekom Germany (3G shut down June 2021), Telia Sweden (3G ended December 2025)
- **Canada**: Rogers, Bell, and Telus shut down 3G networks between 2025-2026

The 3G sunset silently disconnected a generation of connected art. From the late 2000s through the mid-2010s, artists building networked installations, environmental sensor pieces, and location-aware works frequently used 3G cellular modules — they were cheap, widely available, and required no local Wi-Fi infrastructure. These modules were embedded in outdoor installations, remote environmental monitoring artworks, urban intervention pieces, and gallery works designed to transmit data to audiences or web dashboards.

Industry estimates indicated that over 50% of all IoT devices connected via cellular relied exclusively on 2G or 3G networks. Art installations using these modules faced the same fate as millions of commercial IoT devices: they simply stopped transmitting. Unlike a website going offline, where the content may be cached or archived, a networked artwork that loses its data connection loses its core behavior. A sculpture meant to pulse in response to remote sensor data becomes inert. A piece that streamed live readings to a web interface goes silent.

The problem was compounded by the physical nature of these installations. Many were permanently mounted, encased in weatherproof housings, or installed in locations where physical access was difficult. The cellular module was often soldered to a custom circuit board, not a swappable component. Upgrading from 3G to 4G LTE required new hardware, often a complete redesign of the electronics.

## Notes

The 3G shutdown is distinctive because it affected works that their creators may have reasonably expected to function for decades. A cellular network feels like permanent infrastructure in a way that a website or API does not. Artists who embedded 3G modules in long-term installations were making the same assumption as manufacturers of medical alert devices and industrial sensors — that the network would outlast the hardware. It did not.
