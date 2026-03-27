---
title: "Flickr limits free accounts to 1,000 photos, mass deletion begins"
date: "2019-02-05"
end_date: "2019-03-12"
dependency: "Flickr free hosting tier"
event_type: "terms-of-service"
severity: "major"
summary: "After SmugMug acquired Flickr, free accounts were slashed from 1 TB to 1,000 photos. Excess photos were deleted oldest-first starting February 2019, jeopardizing content from 100 million users and breaking projects that relied on Flickr as permanent image hosting."
links:
  - url: "https://techcrunch.com/2018/11/01/flickr-revamps-under-smugmug-with-new-limits-on-free-accounts-unlimited-storage-for-pros/"
    label: "TechCrunch: Flickr revamps under SmugMug"
  - url: "https://time.com/5520636/flickr-delete-photos-export-save/"
    label: "TIME: Flickr is About to Delete Tons of Photos"
  - url: "https://petapixel.com/2019/02/04/flickr-will-delete-photos-tomorrow-if-youre-over-the-new-limit/"
    label: "PetaPixel: Flickr May Delete Photos Tomorrow"
fixes:
  - type: migration
    description: "Users could upgrade to Flickr Pro ($50/year) to retain unlimited storage, or download and re-host their content."
  - type: archive
    description: "Creative Commons and public-domain images uploaded before November 1, 2018 were exempted from deletion."
---

After SmugMug acquired Flickr from Yahoo (via Verizon), free accounts were limited from 1 terabyte of storage to just 1,000 photos and videos. Starting February 2019 (extended to March 12), photos exceeding the limit were deleted oldest-first.

## What changed

Flickr's generous free tier had functioned as de facto permanent image hosting for over a decade. Photography projects, art documentation, Creative Commons archives, and any web content that hotlinked or embedded Flickr-hosted images were at risk. The oldest-first deletion order meant the most historically valuable content was destroyed first.

Creative Commons and public-domain images uploaded before November 2018 were exempted, but "All Rights Reserved" content — including much art photography — was purged. The Flickr API also changed during this period, breaking third-party gallery integrations.

## Notes

The event illustrates the fragility of relying on any platform's free tier as archival storage. When the business model changed, over a decade of assumed permanence evaporated in weeks.
