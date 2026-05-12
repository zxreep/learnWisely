import json
import os
from typing import Any

import requests
from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT, build_framework_prompt

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")


def _call_nvidia(messages: list[dict[str, str]]) -> str:
    if not NVIDIA_API_KEY:
        raise RuntimeError("NVIDIA_API_KEY environment variable is missing")

    resp = requests.post(
        f"{NVIDIA_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {NVIDIA_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": NVIDIA_MODEL,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1800,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"NVIDIA API error {resp.status_code}: {resp.text}")
    return resp.json()["choices"][0]["message"]["content"]


def _safe_json_parse(content: str) -> dict[str, Any]:
    cleaned = content.strip().removeprefix("```json").removesuffix("```").strip()
    parsed = json.loads(cleaned)
    required = ["title", "learner_level", "strategy", "modules", "final_project", "quiz"]
    for key in required:
        if key not in parsed:
            raise RuntimeError(f"Missing key in AI response: {key}")
    if not isinstance(parsed["modules"], list) or not parsed["modules"]:
        raise RuntimeError("AI response must include at least one module")
    return parsed


def generate_learning_framework(topic: str, difficulty: str, article_text: str, source_title: str) -> dict[str, Any]:
    user_prompt = build_framework_prompt(
        topic=topic,
        difficulty=difficulty,
        source_title=source_title,
        article_text=article_text,
    )
    content = _call_nvidia(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )
    return _safe_json_parse(content)
