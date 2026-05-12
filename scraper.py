import re
from functools import lru_cache
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

WIKI_REST_BASE = "https://en.wikipedia.org/api/rest_v1/page"
WIKI_ACTION_API = "https://en.wikipedia.org/w/api.php"
MAX_CHARS = 7000

# Wikipedia may reject generic clients; send a clear UA.
HEADERS = {
    "User-Agent": "LearnWisely/1.0 (https://render.com; educational-api)",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
}

session = requests.Session()
session.headers.update(HEADERS)


def _clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_paragraphs_from_html(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup.select("sup.reference, table, style, script, figure, math, .mw-editsection"):
        tag.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    clean_paragraphs = [_clean_text(p) for p in paragraphs if len(p.strip()) > 50]
    return _clean_text("\n".join(clean_paragraphs))


def _fetch_full_html_via_action_api(page_title: str) -> str:
    """Fallback when REST /html endpoint is unavailable."""
    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
        "formatversion": 2,
        "redirects": 1,
    }
    resp = session.get(WIKI_ACTION_API, params=params, timeout=15)
    if resp.status_code != 200:
        return ""
    data = resp.json()
    return (data.get("parse") or {}).get("text", "")


@lru_cache(maxsize=128)
def get_wikipedia_content(topic: str) -> dict:
    normalized_topic = quote(topic.strip().replace(" ", "_"), safe="_")
    summary_url = f"{WIKI_REST_BASE}/summary/{normalized_topic}"
    html_url = f"{WIKI_REST_BASE}/html/{normalized_topic}"

    summary_resp = session.get(summary_url, timeout=15)
    if summary_resp.status_code != 200:
        raise ValueError(f"Could not find Wikipedia topic: {topic}")

    summary_data = summary_resp.json()
    title = summary_data.get("title", topic)
    extract = summary_data.get("extract", "")

    combined = ""
    html_resp = session.get(html_url, timeout=15)
    if html_resp.status_code == 200:
        combined = _extract_paragraphs_from_html(html_resp.text)

    # Fallback path: fetch page HTML from MediaWiki action API parse endpoint.
    if not combined:
        action_html = _fetch_full_html_via_action_api(title)
        if action_html:
            combined = _extract_paragraphs_from_html(action_html)

    if not combined:
        combined = _clean_text(extract)

    if not combined:
        raise ValueError(f"No useful article content found for: {topic}")

    return {"title": title, "content": combined[:MAX_CHARS]}


@lru_cache(maxsize=128)
def suggest_topics(query: str) -> list[str]:
    params = {
        "action": "opensearch",
        "search": query,
        "limit": 5,
        "namespace": 0,
        "format": "json",
    }
    resp = session.get(WIKI_ACTION_API, params=params, timeout=10)
    if resp.status_code != 200:
        return []
    data = resp.json()
    if isinstance(data, list) and len(data) > 1:
        return data[1]
    return []
