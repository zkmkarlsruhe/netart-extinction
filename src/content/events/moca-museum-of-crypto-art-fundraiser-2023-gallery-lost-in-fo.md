---
title: "MOCA (Museum of Crypto Art) Fundraiser 2023 Gallery Lost in Foundation (foundation.app) Shutdown"
date: "2026-04-27"
dependency: "Foundation (foundation.app) — curated Ethereum NFT marketplace, hosted-gallery frontend, and public-facing IPFS media pinning."
event_type: "platform-shutdown"
summary: "The MOCA (Museum of Crypto Art) Fundraiser 2023 was a call for financial support to keep the museum running. More than 700 artists and creators answered it, and their individual works were afterwards combined into one large, colourful mosaic. Intentionally or not, it became a descendant of \"The Million Dollar Homepage,\" which in 2005 sold a million pixels of screen as advertising space. "
---

The MOCA (Museum of Crypto Art) Fundraiser 2023 was a call for financial support to keep the museum running. More than 700 artists and creators answered it, and their individual works were afterwards combined into one large, colourful mosaic. Intentionally or not, it became a descendant of "The Million Dollar Homepage," which in 2005 sold a million pixels of screen as advertising space. 

Where that page sold the real estate, the MOCA wall gave it away. My contribution, later titled "Vault of the Museum of Crypto Art," is a single photograph. 

I took it in the Copenhagen Metro in June 2023 on a long-obsolete Nikon D3 fitted with a 55 mm f/2.8 lens from around 1989. Old glass and an old sensor, pointed at a piece of very new public infrastructure, so that the photographic past and the technological future meet in one frame. 

I shot it in black and white on purpose, expecting the rest of the fundraiser to arrive saturated with AI and CGI colour, and wanting one quiet grey image to stand in the noise. The work was listed on Foundation (foundation.app). 

On 26 April 2026 Foundation shut down: the company, the front door to its smart contracts, and the public-facing galleries all at once. In its farewell the platform reassured users that their NFTs and their underlying media are not dependent on the Foundation platform.  

That is only half true. The token does survive on Ethereum, but the image it points to was never on Ethereum. It was a file pinned to IPFS, and IPFS only keeps what someone actively chooses to keep. Foundation was that keeper. 

Recent measurements of the public IPFS network (ProbeLab) count roughly 25,000 server nodes, of which only about 4,000 are reliably online at any moment, and both numbers have been declining rather than growing.  None of those nodes is obliged to hold my file. 

The life-giving technology around NFT works is far more fragile than most people assume, because the token can go on pointing serenely at nothing

## Affected artworks

The original version of "[Vault of the Museum of Crypto Art](https://bergholt.net/moca)" by Kasper Bergholt. 

Black and white photograph, Copenhagen Metro, June 2023. 

Archived listing: https://web.archive.org/web/20250322060214/https://foundation.app/mint/eth/0x510af0f5B6C0791d18837a248D2a6340Bf03ad7d/1

## Links

Foundation shutdown statement: https://www.foundation.app/

ARTnews on the closure: https://www.artnews.com/art-news/news/foundation-nft-platform-shutdown-blackdove-sale-failed-1234781419/

The Defiant on the closure: https://thedefiant.io/news/nfts-and-web3/foundation-nft-marketplace-shuts-down-permanently-after-failed-sale

Archived Foundation listing of the work: 

https://web.archive.org/web/20250322060214/https://foundation.app/mint/eth/0x510af0f5B6C0791d18837a248D2a6340Bf03ad7d/1

IPFS network metrics (ProbeLab): https://probelab.io/ipfs/

Reachable Bitcoin node count (Bitnodes): https://bitnodes.io/

## Fixes

The NFTs minted on Foundation are non-custodial and remain on Ethereum regardless of the platform, so collectors can still hold, unlist, and retrieve them. The vulnerable part is the media. Foundation committed to keep pinning the IPFS hosted images and metadata for roughly one year, until about April 2027, after which the files must be re-pinned independently or they will stop resolving. 

Anyone who values a specific piece from the mosaic should back it up and re-pin it, for example through a service such as Pinata or a self-run IPFS node, before that window closes. [The Defiant](https://thedefiant.io/news/nfts-and-web3/foundation-nft-marketplace-shuts-down-permanently-after-failed-sale)

The more durable mitigation is to stop depending on a separate hosting layer at all. Bitcoin Ordinals inscribe the file directly into the witness data of a Bitcoin transaction, with no external URL and no IPFS dependency, and the content is copied in full onto every node that stores the chain. 

As of April 2026 that meant around 23,000 reachable full nodes across more than 170 countries, with many more behind firewalls.

This is the preservation principle behind my related practice as a system poet, where the infrastructure is treated as part of the work.
