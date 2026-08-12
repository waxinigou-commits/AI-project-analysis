# Source and verification policy

## Source tiers

### Tier 1 — first party

- Official product website, documentation, pricing page, changelog, newsroom, repository, or app-store listing
- Official maker/company account or launch announcement

Use Tier 1 for product identity, capabilities, pricing, availability, and launch-date claims.

### Tier 2 — launch/discovery platforms

- Product Hunt public feed and launch pages
- WhatLaunched public directories and launch pages
- V2EX `分享创造` RSS/JSON feeds and posts
- AIHub and other curated AI directories

Use Tier 2 for discovery and source-post timestamps. A directory's “latest” or “added” date is not automatically the product's first launch date.

### Tier 3 — reporting and discussion

- Reputable technology media
- Developer/community discussions with attributable authorship

Use Tier 3 for context, reactions, and independent comparisons. Do not use unattributed reposts to establish critical facts.

## Default public feeds

The bundled collector uses public feeds that are practical for repeatable discovery:

- Product Hunt: `https://www.producthunt.com/feed`
- V2EX 分享创造 RSS: `https://www.v2ex.com/feed/create.xml`
- V2EX 分享创造 JSON Feed: linked from `https://www.v2ex.com/go/create`

Feed availability and formats can change. If a feed fails, report the failure and continue with other sources; do not silently replace it with fabricated data.

## Verification checklist

For each candidate, determine:

1. Is this a usable product rather than an article, event, job, or idea?
2. Is AI core to the product rather than a marketing adjective?
3. What is the canonical product name and website?
4. Does the source describe a first launch, a major update, or merely a mention?
5. Is a date directly supported? Which kind of date is it?
6. Is pricing visible on a first-party page? Capture currency and billing period exactly.
7. Which claims are facts, which are analysis, and which remain unknown?

## Confidence guidance

- **90–100**: canonical site and multiple first-party facts verified; dates and pricing are explicit.
- **70–89**: product identity and key functionality verified; some commercial facts remain undisclosed.
- **50–69**: credible launch lead, but limited first-party detail or ambiguous release timing.
- **Below 50**: keep in review queue; do not promote as verified.

## Access boundaries

- Respect robots, terms, rate limits, and copyright.
- Prefer RSS, JSON Feed, documented APIs, and public pages.
- Do not bypass CAPTCHA, login walls, paywalls, or anti-bot controls.
- Quote sparingly and summarize in original language.
- Store source URLs and retrieval dates so records can be audited later.
