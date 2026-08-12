#!/usr/bin/env python3
"""Collect public product-launch leads without calling an LLM or private API."""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


DEFAULT_SOURCES = (
    ("Product Hunt", "https://www.producthunt.com/feed"),
    ("V2EX 分享创造", "https://www.v2ex.com/feed/create.xml"),
)
AI_TERMS = re.compile(
    r"\b(ai|aigc|agent|agents|agentic|llm|gpt|claude|gemini|deepseek|rag|"
    r"copilot|machine learning|artificial intelligence)\b|"
    r"人工智能|大模型|智能体|生成式|机器学习|深度学习|文生图|文生视频|"
    r"语音合成|智能助手|知识库|向量检索|模型微调|AI\s*原生",
    re.IGNORECASE,
)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def clean_text(value: str) -> str:
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def parse_time(value: str) -> dt.datetime | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError:
        try:
            parsed = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def first_text(node: ET.Element, names: tuple[str, ...]) -> str:
    for name in names:
        found = node.find(name)
        if found is not None and found.text:
            return found.text
    return ""


def entry_url(node: ET.Element) -> str:
    for link in node.findall("{*}link") + node.findall("link"):
        href = link.attrib.get("href", "")
        if href:
            return href
        if link.text and link.text.strip():
            return link.text.strip()
    return ""


def stable_id(source: str, source_url: str, title: str) -> str:
    raw = f"{source}\0{source_url}\0{title}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]


def parse_xml(source: str, xml_text: str, discovered_at: dt.datetime) -> list[dict[str, Any]]:
    root = ET.fromstring(xml_text)
    nodes = root.findall(".//{*}entry")
    if not nodes:
        nodes = root.findall(".//item")
    results: list[dict[str, Any]] = []
    for node in nodes:
        title = clean_text(first_text(node, ("{*}title", "title")))
        body = clean_text(
            first_text(
                node,
                ("{*}content", "{*}summary", "description", "{*}description"),
            )
        )
        url = entry_url(node)
        published_raw = first_text(
            node,
            ("{*}published", "{*}updated", "pubDate", "{*}date"),
        )
        published_at = parse_time(published_raw)
        text = f"{title} {body}"
        results.append(
            {
                "candidate_id": stable_id(source, url, title),
                "title": title,
                "summary": body[:800],
                "source_name": source,
                "source_url": url,
                "source_published_at": published_at.isoformat() if published_at else None,
                "discovered_at": discovered_at.isoformat(),
                "likely_ai": bool(AI_TERMS.search(text)),
                "status": "unverified",
            }
        )
    return [item for item in results if item["title"] and item["source_url"]]


def fetch(url: str, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AI-Product-Growth-Agent/1.0 (public feed collector)",
            "Accept": "application/atom+xml, application/rss+xml, application/xml, text/xml",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def collect(hours: int, timeout: int, include_non_ai: bool) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    now = utc_now()
    cutoff = now - dt.timedelta(hours=hours)
    items: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for source, url in DEFAULT_SOURCES:
        try:
            parsed = parse_xml(source, fetch(url, timeout), now)
        except (urllib.error.URLError, TimeoutError, ET.ParseError) as exc:
            failures.append({"source": source, "url": url, "error": str(exc)})
            continue
        for item in parsed:
            published_at = parse_time(item.get("source_published_at") or "")
            if published_at and published_at < cutoff:
                continue
            if include_non_ai or item["likely_ai"]:
                items.append(item)
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        key = item["source_url"].rstrip("/").lower()
        unique[key] = item
    ordered = sorted(
        unique.values(),
        key=lambda item: item.get("source_published_at") or item["discovered_at"],
        reverse=True,
    )
    return ordered, failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect AI product leads from public launch feeds. No LLM or API key is used."
    )
    parser.add_argument("--hours", type=int, default=48, help="lookback window; default: 48")
    parser.add_argument("--timeout", type=int, default=25, help="per-feed timeout seconds")
    parser.add_argument("--output", type=Path, help="write JSON to this path; stdout if omitted")
    parser.add_argument(
        "--include-non-ai",
        action="store_true",
        help="include all launch leads and let Codex classify them",
    )
    args = parser.parse_args()
    if args.hours <= 0 or args.timeout <= 0:
        parser.error("--hours and --timeout must be positive")

    items, failures = collect(args.hours, args.timeout, args.include_non_ai)
    payload = {
        "generated_at": utc_now().isoformat(),
        "lookback_hours": args.hours,
        "candidate_count": len(items),
        "candidates": items,
        "source_failures": failures,
        "notice": "Candidates are unverified leads. Codex must verify them before analysis or promotion.",
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {len(items)} candidates to {args.output}")
    else:
        sys.stdout.write(rendered)
    return 0 if items or not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
