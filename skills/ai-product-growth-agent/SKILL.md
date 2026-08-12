---
name: ai-product-growth-agent
description: Collect, verify, analyze, and promote newly launched AI products with Codex only. Use when users ask to discover daily AI launches, build an AI product radar, research a new product, create commercialization analysis, generate platform-specific launch or growth content, prepare a multi-channel campaign, or publish reviewed promotional drafts through authorized browser sessions. Does not require OPENAI_API_KEY.
---

# AI Product Growth Agent

Run an evidence-first workflow that turns public launch signals into verified product records and reviewable promotion campaigns. Use Codex reasoning for classification, analysis, and writing; use the bundled script only for deterministic feed collection and normalization.

## Choose a mode

- **Radar**: collect and rank newly launched AI products.
- **Research**: verify and analyze one named product.
- **Campaign**: generate differentiated promotion drafts for a verified product.
- **Publish**: publish approved drafts through already-authorized tools or browser sessions.
- **Daily run**: run Radar, select the strongest products, then generate Campaign drafts.

For source coverage and verification rules, read [references/sources.md](references/sources.md). For campaign work or publishing, also read [references/promotion.md](references/promotion.md). Read [references/schemas.md](references/schemas.md) when writing machine-readable artifacts.

## Radar workflow

1. Run the collector from the skill directory:

   ```bash
   python3 scripts/collect_sources.py --hours 48 --output <workspace>/outputs/product-candidates.json
   ```

2. Treat every collected item as a lead, not a verified fact. Remove duplicates by canonical website, normalized name, and source URL.
3. Keep likely AI products. Exclude generic news, job posts, events, courses, prompt collections without a product, and updates with no usable product.
4. Open the launch page and the product's first-party website. Prefer official pricing, documentation, changelog, app-store listing, or company announcement as additional evidence.
5. Separate timestamps:
   - `source_published_at`: when the source post appeared;
   - `first_launch_at`: the earliest verified first-party launch date;
   - `discovered_at`: when this workflow found the item.
6. Label unknown facts `未披露`. Never infer funding, revenue, customers, pricing, founders, or traction.
7. Score candidates using the schema. Explain every score with evidence or clearly labeled analysis.
8. Write verified records and a short daily digest. Include direct source links.

If a source requires CAPTCHA, login, or human verification, do not bypass it. Use an available RSS/feed, another public first-party source, or mark the field for manual review.

## Research workflow

1. Resolve the official product identity and canonical website.
2. Gather at least two sources where practical, including at least one first-party source.
3. Capture positioning, capabilities, intended users, pricing evidence, and release evidence.
4. Mark statements as either `fact`, `analysis`, or `unknown`.
5. Produce:
   - a concise product brief;
   - commercialization analysis;
   - competitors and differentiation;
   - growth opportunities and risks;
   - confidence score and unresolved questions.
6. Avoid presenting competitor selection, market opportunity, or business-model interpretation as company-confirmed facts.

## Campaign workflow

1. Require a verified product record or verify the product first.
2. Identify one real audience problem and one evidence-backed product promise. Do not invent usage numbers, testimonials, discounts, or scarcity.
3. Generate genuinely adapted drafts, not identical cross-posts:
   - short discovery post;
   - maker/community post;
   - professional analysis post;
   - long-form educational post;
   - optional launch digest entry.
4. Add one canonical destination and channel-specific UTM parameters.
5. Include a disclosure when the author has a commercial relationship with the product.
6. Run the quality and safety checklist in `references/promotion.md`.
7. Save all drafts with status `draft` and present a compact approval table.

## Publish workflow

Publishing is an external side effect. Never publish merely because the user asked to generate or automate content.

1. Show the exact final copy, destination account, platform, link, and media before publishing.
2. Obtain explicit user approval for the specified posts or an already-defined approved batch.
3. Use only authorized connectors or the user's signed-in browser session.
4. Do not bypass CAPTCHAs, platform limits, moderation, or anti-spam protections.
5. Stop if the account, audience, or product identity is ambiguous.
6. After publishing, record the final URL, timestamp, account, and exact copy. Never claim success without a confirmed URL or platform acknowledgement.

Scheduling may automatically collect, analyze, and prepare drafts. Default scheduled work must stop at `draft`; unattended publishing requires a separately documented user-approved channel policy and platform-supported authorization.

## Output requirements

- Lead with what is new and why it matters.
- Cite direct pages, not search result pages.
- Distinguish source facts from Codex analysis visibly.
- Prefer fewer high-confidence products over a large noisy list.
- Preserve Chinese and original product names when both are useful.
- Never expose private account data, cookies, tokens, or unpublished business information.

## Common user prompts

- “收集过去 24 小时国内外新发布的 AI 产品，给我前 10 名。”
- “核验这个产品的发布日期、定价和目标用户。”
- “给这个产品生成小红书、知乎、V2EX 和 X 的推广草稿。”
- “把已审核的三条内容发到我当前登录的账号。”
- “每天生成 AI 新产品日报和待审核推广包，不要自动发布。”
