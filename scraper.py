import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

WIKI_REST_BASE = "https://en.wikipedia.org/api/rest_v1/page"
WIKI_ACTION_API = "https://en.wikipedia.org/w/api.php"
MAX_CHARS = 7000


def _clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


@lru_cache(maxsize=128)
def get_wikipedia_content(topic: str) -> dict:
    normalized_topic = topic.strip().replace(" ", "_")
    summary_url = f"{WIKI_REST_BASE}/summary/{normalized_topic}"
    html_url = f"{WIKI_REST_BASE}/html/{normalized_topic}"

    summary_resp = requests.get(summary_url, timeout=12)
    if summary_resp.status_code != 200:
        raise ValueError(f"Could not find Wikipedia topic: {topic}")

    summary_data = summary_resp.json()
    title = summary_data.get("title", topic)

    html_resp = requests.get(html_url, timeout=12)
    if html_resp.status_code != 200:
        extract = summary_data.get("extract", "")
        if not extract:
            raise ValueError(f"No useful article content found for: {topic}")
        return {"title": title, "content": extract[:MAX_CHARS]}

    soup = BeautifulSoup(html_resp.text, "html.parser")

    for tag in soup.select("sup.reference, table, style, script, figure, math, .mw-editsection"):
        tag.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    clean_paragraphs = [_clean_text(p) for p in paragraphs if len(p.strip()) > 50]
    combined = "\n".join(clean_paragraphs)

    if not combined:
        combined = summary_data.get("extract", "")

    combined = _clean_text(combined)
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
    resp = requests.get(WIKI_ACTION_API, params=params, timeout=10)
    if resp.status_code != 200:
        return []
    data = resp.json()
    if isinstance(data, list) and len(data) > 1:
        return data[1]
    return []
