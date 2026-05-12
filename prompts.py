SYSTEM_PROMPT = """
You are a world-class beginner teacher and curriculum designer.
You design practical learning frameworks from beginner to expert.

Rules:
- Keep explanations clear and structured.
- Adapt depth to requested difficulty: overview, mediocre, expert.
- Use both source content and general knowledge when needed.
- Return ONLY valid JSON (no markdown fences).
""".strip()


def build_framework_prompt(topic: str, difficulty: str, source_title: str, article_text: str) -> str:
    return f"""
Topic requested: {topic}
Difficulty: {difficulty}
Source title: {source_title}

Source material:
{article_text}

Create a learning framework. Return strict JSON with this schema:
{{
  "title": "string",
  "learner_level": "overview|mediocre|expert",
  "strategy": "string",
  "modules": [
    {{
      "topic": "string",
      "summary": "string",
      "subtopics": [
        {{"name": "string", "objective": "string", "estimated_hours": 1}}
      ]
    }}
  ],
  "final_project": "string",
  "quiz": [
    {{"question": "string", "answer": "string"}},
    {{"question": "string", "answer": "string"}},
    {{"question": "string", "answer": "string"}}
  ]
}}

Planning rules by difficulty:
- overview: 3-4 modules, 2-3 subtopics per module, fast conceptual path.
- mediocre: 5-7 modules, 3-4 subtopics per module, balanced theory + practice.
- expert: 8-10 modules, 4-6 subtopics per module, advanced depth and project focus.

Additional rules:
- Each module must have a clear topic and summary.
- Subtopics must be practical and progressive.
- `estimated_hours` should be a positive integer.
- quiz must contain exactly 3 question-answer pairs.
- no extra keys.
""".strip()
