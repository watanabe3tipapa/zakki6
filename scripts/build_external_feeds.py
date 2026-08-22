#!/usr/bin/env python3
"""Build the external-source sections used by the zakki6 landing page.

Only title, publication date, category and canonical link are republished from
public official RSS feeds. Article bodies and media are never copied.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import os
import re
from email.utils import parsedate_to_datetime
from html import escape
from pathlib import Path
from time import sleep
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "_includes" / "external-feeds.md"
JST = ZoneInfo("Asia/Tokyo")
USER_AGENT = "zakki6-external-feed-builder/1.0 (+https://github.com/watanabe3tipapa/zakki6)"
FEED_TIMESTAMP = re.compile(r"\[\d{4}\.\d{2}\.\d{2} \d{2}:\d{2} JST 取得\]\{\.feed-updated\}")


@dataclass(frozen=True)
class FeedConfig:
    section_id: str
    label: str
    source_name: str
    source_url: str
    feed_url: str
    allowed_host: str
    description: str
    item_limit: int = 3


@dataclass(frozen=True)
class FeedItem:
    title: str
    url: str
    published: str
    category: str


FEEDS = (
    FeedConfig(
        section_id="trend",
        label="TREND",
        source_name="MdN Design Interactive",
        source_url="https://www.mdn.co.jp/news",
        feed_url="https://www.mdn.co.jp/feed/index.xml",
        allowed_host="www.mdn.co.jp",
        description="MdNの公式フィードから、デザインとクリエイティブの最新トピックをピックアップ。",
    ),
    FeedConfig(
        section_id="antenna",
        label="ANTENNA",
        source_name="デジタル庁",
        source_url="https://www.digital.go.jp/news",
        feed_url="https://www.digital.go.jp/rss/news.xml",
        allowed_host="www.digital.go.jp",
        description="デジタル庁の公式新着・更新から、政策・サービス・行政DXの最新情報を受信。",
    ),
)


def text_of(parent: ET.Element, name: str) -> str:
    child = parent.find(name)
    return (child.text or "").strip() if child is not None else ""


def fetch_xml(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/xml, text/xml"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                return response.read()
        except Exception as error:  # Network failures must fail the build after retrying.
            last_error = error
            if attempt < 2:
                sleep(2**attempt)
    raise RuntimeError(f"Could not retrieve {url}: {last_error}")


def is_allowed_url(url: str, allowed_host: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname == allowed_host


def display_date(raw_date: str) -> str:
    try:
        return parsedate_to_datetime(raw_date).astimezone(JST).strftime("%Y.%m.%d")
    except (TypeError, ValueError, IndexError):
        return raw_date


def read_items(config: FeedConfig) -> list[FeedItem]:
    root = ET.fromstring(fetch_xml(config.feed_url))
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError(f"RSS channel missing: {config.feed_url}")

    items: list[FeedItem] = []
    for node in channel.findall("item"):
        title = text_of(node, "title")
        url = text_of(node, "link")
        published = text_of(node, "pubDate")
        category = text_of(node, "category") or "最新情報"
        if title and published and is_allowed_url(url, config.allowed_host):
            items.append(FeedItem(title=title, url=url, published=display_date(published), category=category))
        if len(items) == config.item_limit:
            break

    if len(items) < config.item_limit:
        raise RuntimeError(f"Insufficient valid RSS entries from {config.feed_url}")
    return items


def render_items(items: Iterable[FeedItem]) -> str:
    rows = []
    for index, item in enumerate(items, start=1):
        rows.append(
            """::: {{.feed-item}}
[{index:02d}]{{.feed-index}}

::: {{.feed-copy}}
[{category} · {published}]{{.feed-meta}}

[{title}]({url}){{.feed-title target=\"_blank\" rel=\"noreferrer\"}}
:::

[↗]({url}){{.feed-arrow target=\"_blank\" rel=\"noreferrer\"}}
:::""".format(
                index=index,
                url=escape(item.url, quote=True),
                category=escape(item.category),
                published=escape(item.published),
                title=escape(item.title),
            )
        )
    return "\n\n".join(rows)


def render_section(config: FeedConfig, items: list[FeedItem], retrieved_at: str) -> str:
    return """::: {{.external-feed .content-card .feed-card #{section_id}}}
[LIVE / 03]{{.feed-card-index}}

::: {{.card-topline}}
[{label}]{{.card-role}}

[{source_name}]{{.card-kind}}
:::

### {label} {{#{section_id}-heading}}

{description}

::: {{.feed-list}}
{items}
:::

::: {{.feed-footer}}
[{retrieved_at} JST 取得]{{.feed-updated}}

[すべて見る ↗]({source_url}){{.feed-source target=\"_blank\" rel=\"noreferrer\"}}
:::
:::""".format(
        section_id=config.section_id,
        label=config.label,
        source_name=escape(config.source_name),
        source_url=escape(config.source_url, quote=True),
        description=escape(config.description),
        items=render_items(items),
        retrieved_at=retrieved_at,
    )


def stable_content(markdown: str) -> str:
    """Ignore the retrieval timestamp when deciding whether a publication is needed."""
    return FEED_TIMESTAMP.sub("[retrieved timestamp]{.feed-updated}", markdown)


def report_change(changed: bool) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with Path(github_output).open("a", encoding="utf-8") as output:
            output.write(f"changed={'true' if changed else 'false'}\n")


def main() -> None:
    retrieved_at = datetime.now(JST).strftime("%Y.%m.%d %H:%M")
    sections = [render_section(config, read_items(config), retrieved_at) for config in FEEDS]
    generated = "\n\n".join(sections) + "\n"
    existing = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
    changed = stable_content(generated) != stable_content(existing)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if changed:
        OUTPUT_PATH.write_text(generated, encoding="utf-8")

    report_change(changed)
    state = "updated" if changed else "unchanged"
    print(f"Official feeds {state}: {len(FEEDS)} sources, changed={str(changed).lower()}.")


if __name__ == "__main__":
    main()
