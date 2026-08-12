#!/usr/bin/env python3
import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / "public/data/products.json").read_text())
required = {"id", "name", "tagline", "source", "sourceUrl", "website", "launchedAt", "verifiedAt", "factStatus", "analysisNote", "confidence"}
errors: list[str] = []
seen: set[str] = set()

for index, product in enumerate(products):
    label = product.get("name", f"row {index}")
    missing = required - product.keys()
    if missing:
        errors.append(f"{label}: missing {sorted(missing)}")
    if product.get("id") in seen:
        errors.append(f"{label}: duplicate id")
    seen.add(product.get("id", ""))
    for field in ("sourceUrl", "website"):
        parsed = urlparse(product.get(field, ""))
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{label}: invalid {field}")
    if product.get("source") == "WhatLaunched" and "/en/launch/" not in product.get("sourceUrl", ""):
        errors.append(f"{label}: sourceUrl must be a direct launch page")
    for field in ("launchedAt", "verifiedAt"):
        try:
            dt.date.fromisoformat(product.get(field, ""))
        except ValueError:
            errors.append(f"{label}: invalid {field}")
    if product.get("factStatus") != "已核验":
        errors.append(f"{label}: factStatus is not verified")
    if not 0 <= int(product.get("confidence", -1)) <= 100:
        errors.append(f"{label}: confidence out of range")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"validated {len(products)} verified products")
