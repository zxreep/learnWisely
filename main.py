from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ai import generate_learning_framework
from scraper import get_wikipedia_content, suggest_topics

app = FastAPI(title="LearnWisely API", version="2.0.0")

Difficulty = Literal["overview", "mediocre", "expert"]


class LearnRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=100, description="Topic to learn")
    difficulty: Difficulty = Field(default="overview", description="Learning depth")


class SubtopicItem(BaseModel):
    name: str
    objective: str
    estimated_hours: int


class TopicModule(BaseModel):
    topic: str
    summary: str
    subtopics: list[SubtopicItem]


class LearnFrameworkResponse(BaseModel):
    title: str
    learner_level: Difficulty
    strategy: str
    modules: list[TopicModule]
    final_project: str
    quiz: list[dict[str, str]]


@app.get("/")
def health_check() -> dict:
    return {"status": "running"}


@app.get("/suggestions")
def topic_suggestions(q: str) -> dict:
    if len(q.strip()) < 2:
        return {"suggestions": []}
    return {"suggestions": suggest_topics(q.strip())}


@app.post("/learn", response_model=LearnFrameworkResponse)
def learn_topic(payload: LearnRequest):
    topic = payload.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    try:
        article = get_wikipedia_content(topic)
        result = generate_learning_framework(
            topic=topic,
            difficulty=payload.difficulty,
            article_text=article["content"],
            source_title=article["title"],
        )
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate framework: {exc}") from exc
