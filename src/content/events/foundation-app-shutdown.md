---
title: "Foundation NFT platform shuts down, IPFS media pinning ends April 2027"
date: "2026-04-27"
dependency: "Foundation (foundation.app) — curated Ethereum platform for tokenized digital art, hosted-gallery frontend, and IPFS media availability via Foundation-operated gateway and pinning infrastructure"
event_type: "platform-shutdown"
severity: "major"
summary: "Foundation, a curated Ethereum platform for tokenized digital art, went offline in April 2026 after a failed acquisition; its tokens persist on-chain, but IPFS-hosted media loses its key pinning provider when Foundation's gateway support ends on 27 April 2027."
links:
  - url: "https://www.foundation.app/"
    label: "Foundation closing statement (27 April 2026)"
  - url: "https://thedefiant.io/news/nfts-and-web3/foundation-nft-marketplace-shuts-down-permanently-after-failed-sale"
    label: "The Defiant: Foundation NFT marketplace shuts down permanently after failed sale"
  - url: "https://www.artnews.com/art-news/news/foundation-nft-platform-shutdown-blackdove-sale-failed-1234781419/"
    label: "ARTnews: Foundation NFT platform shutdown after BlackDove sale failed"
  - url: "https://web.archive.org/web/20250322060214/https://foundation.app/mint/eth/0x510af0f5B6C0791d18837a248D2a6340Bf03ad7d/1"
    label: "Archived Foundation listing of an affected work (Wayback Machine)"
  - url: "https://probelab.io/ipfs/"
    label: "IPFS network measurements (ProbeLab)"
affected_artworks:
  - artwork: "vault-of-the-museum-of-crypto-art"
    severity: major
    status: degraded
    note: "Independently minted and listed on Foundation. Token persists on Ethereum, but the IPFS-hosted media depends on independent re-pinning before Foundation's gateway support ends in April 2027."
fixes:
  - type: workaround
    description: "Tokens and contracts are non-custodial and remain on Ethereum regardless of the platform. Works still held in escrow via Foundation's on-chain listing contracts must be manually delisted; community-built delisting tools are referenced in the closing statement."
  - type: migration
    description: "Media previously relying on Foundation's IPFS infrastructure should be independently re-pinned, mirrored, or otherwise preserved — through any IPFS pinning service, institutional archive, or self-hosted node — before Foundation's gateway support ends on 27 April 2027."
  - type: archive
    description: "Snapshots of individual listing pages exist in the Wayback Machine, and further pages can be archived while cached copies remain accessible."
---

On 27 April 2026, Foundation (foundation.app) published a closing statement confirming that the platform would remain offline indefinitely. A curated Ethereum platform for tokenized digital art that had facilitated roughly $230 million in primary sales, Foundation went offline in April 2026 after a planned acquisition by the digital-art display company BlackDove fell through. The shutdown removed the web frontend, public listing pages, and hosted gallery views.

## What changed

Tokens minted on Foundation are non-custodial and persist on Ethereum independently of the platform. The media they reference, however, was commonly served through IPFS with Foundation acting as a key provider of gateway and pinning infrastructure. Foundation's closing statement asserts that "NFTs and their underlying media are not dependent on the Foundation platform" — which holds for the tokens and smart contracts, but not automatically for media availability.

IPFS content remains retrievable only while at least one provider continues to make the referenced blocks available; active pinning is the standard way to ensure that availability over time. Public IPFS network measurements from ProbeLab document changing DHT and server-node conditions, underscoring that availability depends on active network participation.

Foundation has committed to maintaining its IPFS gateway through 27 April 2027, one year from its closing statement. Media and metadata that have not been independently re-pinned or mirrored by then risk becoming unreachable through Foundation-dependent paths, leaving on-chain tokens that point to content no longer reliably available.

## Notes

The shutdown affects works whose listings, gallery views, and media availability depended on Foundation. One documented example is "Vault of the Museum of Crypto Art" (Kasper Bergholt, 2023), a black-and-white photograph independently minted and listed on Foundation. Works minted through other infrastructure are not necessarily at risk: the 713-artist Museum of Crypto Art 2023 fundraiser mosaic, for instance, was minted through Manifold on Ethereum with contributor tokens on Polygon and redundant media storage, and so does not depend on Foundation's pinning.
