---
ai_generated: true
title: "Google+ consumer platform shut down"
date: "2019-04-02"
dependency: "Google+ platform and APIs"
event_type: "platform-shutdown"
severity: "total"
summary: "Google shut down consumer Google+ on April 2, 2019, deleting all content and disabling APIs. Web integrations — +1 buttons, Google+ sign-in, sharing widgets, and interactive posts — all ceased to function across millions of sites."
links:
  - url: "https://developers.googleblog.com/en/google-apis-shutting-down-march-7-2019/"
    label: "Google Developers Blog: Google+ APIs shutting down"
fixes:
  - type: none
    description: "All consumer Google+ content was permanently deleted. No archive was provided beyond a personal data export tool available before shutdown."
---

Google shut down the consumer version of Google+ on April 2, 2019, permanently deleting all content from consumer accounts and Google+ pages. The Google+ APIs had been shut down earlier, on March 7, 2019.

## What changed

The shutdown was accelerated after two security bugs exposed private profile data. Beyond the platform content itself, the shutdown broke web-wide integrations: +1 buttons embedded across millions of sites, Google+ sign-in flows used for authentication, sharing widgets, and interactive posts all stopped functioning. Sites that had implemented "Sign in with Google+" needed to migrate to Google's separate OAuth system.

## Notes

Google+ had been deeply integrated into other Google products — YouTube comments, Google Photos, and Blogger all had Google+ dependencies that needed to be unwound. The shutdown is notable as one of the largest single-platform content deletions by a major technology company.
