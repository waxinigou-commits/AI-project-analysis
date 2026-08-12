# Artifact schemas

## Product record

Write UTF-8 JSON. Use `null` for unknown scalar facts and empty arrays for no evidence.

```json
{
  "id": "normalized-product-id",
  "name": "Product name",
  "original_name": "Product name",
  "canonical_url": "https://example.com/",
  "source_url": "https://source.example/item",
  "source_name": "V2EX",
  "source_published_at": "2026-08-12T01:23:45Z",
  "first_launch_at": null,
  "discovered_at": "2026-08-12T02:00:00Z",
  "kind": "new_product",
  "ai_relevance": 92,
  "category": "AI 编程",
  "tagline": "Source-backed short description",
  "facts": [
    {
      "claim": "A verifiable statement",
      "source_url": "https://example.com/docs",
      "retrieved_at": "2026-08-12"
    }
  ],
  "pricing": {
    "status": "verified|undisclosed|unavailable",
    "summary": "来源未披露",
    "source_url": null
  },
  "analysis": {
    "target_users": [],
    "positioning": "",
    "business_model": "",
    "competitors": [],
    "opportunities": [],
    "risks": []
  },
  "confidence": 80,
  "review_status": "verified|needs_review|rejected"
}
```

`kind` must be one of `new_product`, `major_update`, `minor_update`, or `mention`.

## Campaign draft

```json
{
  "campaign_id": "product-slug_2026_08",
  "product_id": "normalized-product-id",
  "core_message": {
    "audience": "",
    "problem": "",
    "promise": "",
    "proof": [""],
    "limitation": ""
  },
  "drafts": [
    {
      "platform": "xiaohongshu",
      "account": null,
      "status": "draft",
      "copy": "",
      "destination_url": "",
      "media": [],
      "disclosure": null,
      "scheduled_at": null,
      "published_url": null
    }
  ]
}
```

Allowed status progression:

```text
draft -> approved -> publishing -> published
                     \-> failed
draft/approved -> canceled
```

Never set `published` without a confirmed platform URL or acknowledgement.
