SYSTEM_PROMPT = """
You are a world-class beginner teacher who explains difficult topics simply.

Rules:
- Avoid jargon; if you use a hard word, define it in plain words.
- Explain step-by-step in a friendly way.
- Keep the explanation accurate, engaging, and educational.
- Write for complete beginners and children around age 10.
- Return ONLY valid JSON.
- Do not include markdown fences.
""".strip()


def build_user_prompt(topic: str, source_title: str, article_text: str, extra_simple: bool = False) -> str:
    simple_rule = "Use extra short sentences and very simple words." if extra_simple else ""
    return f"""
Topic: {topic}
Source title: {source_title}

Use the following Wikipedia content to create a learning guide:
{article_text}

Return STRICT JSON with this schema:
{{
  "title": "string",
  "simple_explanation": "string",
  "learning_roadmap": ["step 1", "step 2", "step 3"],
  "analogy": "string",
  "quiz": [
    {{"question": "string", "answer": "string"}},
    {{"question": "string", "answer": "string"}},
    {{"question": "string", "answer": "string"}}
  ]
}}

Additional rules:
- learning_roadmap should have 4-6 practical steps.
- quiz should contain exactly 3 beginner questions.
- answer in English.
- no extra keys.
{simple_rule}
""".strip()
