---
ai_generated: true
wikipedia: "https://en.wikipedia.org/wiki/Freenode"
title: "Freenode IRC network collapses after hostile takeover and database wipe"
date: "2021-06-14"
dependency: "Freenode IRC network"
event_type: "network-shutdown"
severity: "total"
summary: "Freenode, the largest IRC network for open-source and creative communities, suffered a hostile takeover followed by a complete database wipe on June 14, 2021, destroying decades of channel registrations, community structures, and chat history."
links:
  - url: "https://en.wikipedia.org/wiki/Freenode"
    label: "Wikipedia: Freenode"
  - url: "https://www.devever.net/~hl/freenode_suicide"
    label: "Freenode commits suicide, is no longer a serious IRC network"
  - url: "https://www.jeffgeerling.com/blog/2021/freenode-dead-long-live-irc"
    label: "Jeff Geerling: Freenode is dead. Long live IRC?"
fixes:
  - type: migration
    description: "Most communities migrated to Libera Chat, a new network launched May 19, 2021 by former Freenode staff. Channel names and community structures had to be manually re-established."
  - type: none
    description: "Chat logs, channel histories, and community metadata accumulated over nearly two decades were permanently lost in the database wipe."
---

On June 14, 2021, Freenode's new management performed an unannounced infrastructure reset, migrating the entire network to new software (InspIRCd and Anope) and wiping all previous data. Every nickname registration, channel registration, and access list accumulated since Freenode's founding in 1995 was erased.

## What changed

The collapse followed a months-long crisis. In 2017, Freenode's head of staff had quietly transferred ownership to Andrew Lee, founder of Private Internet Access. When this arrangement became publicly contentious in May 2021, at least 14 volunteer staff members resigned. The new management then began seizing channels belonging to projects that announced moves to other networks, citing "policy violations" — a move widely perceived as retaliation.

Freenode had been the de facto home for thousands of open-source projects and creative communities. Channels dedicated to creative coding, digital art tooling, livecoding, demoscene activity, and collaborative art projects lost their accumulated community infrastructure overnight. The IRC model meant that channel history, operator hierarchies, ban lists, and community governance structures existed only on the network's services database — there was no export, no backup, no migration path.

By August 2021, over a thousand projects had departed. Ubuntu, Fedora, Arch Linux, Debian, FreeBSD, Gentoo, KDE, the Wikimedia Foundation, and hundreds of others relocated to Libera Chat. Creative communities that had used Freenode channels as coordination hubs — for projects like livecoding environments, generative art tools, and collaborative net art — had to rebuild their social infrastructure from scratch.

## Notes

The Freenode collapse illustrates how network-layer social infrastructure can be destroyed even when the underlying protocol (IRC) remains functional. The loss was not of content or code but of accumulated community structure: who had voice, who had ops, which bots ran which services, which channel topics contained which institutional memory. These governance layers, invisible until they vanished, had been built over decades and could not be recreated by simply joining a new server.
