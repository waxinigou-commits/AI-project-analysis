#!/usr/bin/env python3
"""Collect public AI product launches and enrich them with GitHub Models.

The public site reads public/data/products.json. SQLite is the durable,
versioned analytical store; JSON is a static deployment snapshot.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import sqlite3
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "public/data/products.json"
DB_PATH = ROOT / "data/products.db"
PH_FEED = "https://www.producthunt.com/feed"
WHAT_LAUNCHED = "https://whatlaunched.today/en/tags/ai"
MODEL_URL = "https://models.github.ai/inference/chat/completions"

SYSTEM_PROMPT = """你是谨慎的 AI 产品商业分析师。只根据输入事实做判断，不得虚构融资、收入、客户或价格。未披露价格时 pricing 必须写“来源未披露”；推测字段必须用“分析：”或“推测”标明。输出一个 JSON 对象，字段严格为：category(string), score(0-100 integer), pricing(string), pricingModel(string), targetUsers(string array), positioning(string), businessModel(string), competitors(string array), opportunities(string array), risks(string array), signals(string array), confidence(0-100 integer), analysisNote(string)。所有文字用简体中文，数组各 2-4 项。"""


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "AI-Signal/1.0 (+GitHub Actions)"})
    with urllib.request.urlopen(req, timeout=25) as res:
        return res.read().decode("utf-8", "replace")


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "product"


def clean(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def collect_product_hunt() -> list[dict]:
    root = ET.fromstring(fetch(PH_FEED))
    items: list[dict] = []
    for entry in root.findall(".//{*}entry")[:30]:
        name = clean(entry.findtext("{*}title", ""))
        raw_content = html.unescape(entry.findtext("{*}content", ""))
        first_paragraph = re.search(r"<p>(.*?)</p>", raw_content, re.S)
        description = clean(first_paragraph.group(1) if first_paragraph else raw_content)
        link_node = entry.find("{*}link")
        url = link_node.attrib.get("href", "") if link_node is not None else ""
        published = entry.findtext("{*}published", "")[:10] or dt.date.today().isoformat()
        if name and any(x in (name + " " + description).lower() for x in ("ai", "agent", "llm", "gpt", "claude")):
            items.append({"id": slug(name), "name": name, "tagline": description[:180], "source": "Product Hunt", "sourceUrl": url, "website": "", "launchedAt": published})
    return items


class WhatLaunchedParser(HTMLParser):
    """Extract only complete, directly verifiable launch cards."""
    def __init__(self) -> None:
        super().__init__()
        self.cards: list[dict] = []
        self.current: dict | None = None
        self.capture: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        href = values.get("href", "") or ""
        classes = values.get("class", "") or ""
        if tag == "a" and href.startswith("/en/launch/") and "font-medium" in classes:
            self.current = {"sourceUrl": "https://whatlaunched.today" + href}
            self.capture = "name"
        elif self.current and tag == "p" and "line-clamp-2" in classes:
            self.capture = "tagline"
        elif self.current and tag == "time" and values.get("datetime"):
            self.current["launchedAt"] = values["datetime"]
        elif self.current and tag == "a" and href.startswith("http") and values.get("target") == "_blank":
            self.current["website"] = href

    def handle_data(self, data: str) -> None:
        if self.current and self.capture in ("name", "tagline"):
            self.current[self.capture] = (self.current.get(self.capture, "") + data).strip()

    def handle_endtag(self, tag: str) -> None:
        if tag in ("a", "p"):
            self.capture = None
        if tag == "div" and self.current and all(self.current.get(k) for k in ("name", "tagline", "sourceUrl", "website", "launchedAt")):
            item = self.current
            item.update({"id": slug(item["name"]), "source": "WhatLaunched"})
            self.cards.append(item)
            self.current = None


def collect_whatlaunched() -> list[dict]:
    parser = WhatLaunchedParser()
    parser.feed(fetch(WHAT_LAUNCHED))
    unique = {item["id"]: item for item in parser.cards}
    return list(unique.values())[:30]


def analyze(item: dict, token: str) -> dict:
    payload = json.dumps({"model": os.getenv("GITHUB_MODEL", "openai/gpt-4.1-mini"), "temperature": 0.2, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": json.dumps(item, ensure_ascii=False)}]}).encode()
    req = urllib.request.Request(MODEL_URL, data=payload, method="POST", headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=60) as res:
        response = json.load(res)
    return json.loads(response["choices"][0]["message"]["content"])


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
      CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY, name TEXT NOT NULL, source TEXT NOT NULL,
        source_url TEXT, launched_at TEXT, category TEXT, score INTEGER,
        payload TEXT NOT NULL, analyzed_at TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS idx_products_launched_at ON products(launched_at DESC);
      CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
    """)


def main() -> None:
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(JSON_PATH.read_text()) if JSON_PATH.exists() else []
    known = {p["id"]: p for p in existing}
    candidates: list[dict] = []
    for collector in (collect_product_hunt, collect_whatlaunched):
        try:
            candidates.extend(collector())
        except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
            print(f"warning: {collector.__name__} failed: {exc}")
    token = os.getenv("GITHUB_TOKEN", "")
    for item in candidates:
        if item["id"] in known:
            continue
        if not token:
            print(f"skip {item['name']}: GITHUB_TOKEN unavailable")
            continue
        try:
            known[item["id"]] = {**item, **analyze(item, token), "verifiedAt": dt.date.today().isoformat(), "factStatus": "已核验"}
            print(f"analyzed {item['name']}")
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as exc:
            print(f"warning: analysis failed for {item['name']}: {exc}")
    products = sorted(known.values(), key=lambda p: p["launchedAt"], reverse=True)
    JSON_PATH.write_text(json.dumps(products, ensure_ascii=False, indent=2) + "\n")
    with sqlite3.connect(DB_PATH) as conn:
        init_db(conn)
        active_ids = [p["id"] for p in products]
        if active_ids:
            placeholders = ",".join("?" for _ in active_ids)
            conn.execute(f"DELETE FROM products WHERE id NOT IN ({placeholders})", active_ids)
        for product in products:
            conn.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload, score=excluded.score, category=excluded.category, analyzed_at=excluded.analyzed_at", (product["id"], product["name"], product["source"], product.get("sourceUrl", ""), product["launchedAt"], product.get("category", ""), product.get("score", 0), json.dumps(product, ensure_ascii=False), dt.datetime.now(dt.timezone.utc).isoformat()))
        conn.commit()
    print(f"snapshot: {len(products)} products")


if __name__ == "__main__":
    main()
