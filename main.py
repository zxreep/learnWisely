from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ai import generate_learning_guide, simplify_existing_guide
from scraper import get_wikipedia_content, suggest_topics

app = FastAPI(title="LearnWisely API", version="1.0.0")


class LearnRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=100, description="Topic to learn")


class QuizItem(BaseModel):
    question: str
    answer: str


class LearnResponse(BaseModel):
    title: str
    simple_explanation: str
    learning_roadmap: list[str]
    analogy: str
    quiz: list[QuizItem]


@app.get("/")
def health_check() -> dict:
    return {"status": "running"}


@app.get("/suggestions")
def topic_suggestions(q: str) -> dict:
    if len(q.strip()) < 2:
        return {"suggestions": []}
    return {"suggestions": suggest_topics(q.strip())}


@app.post("/learn", response_model=LearnResponse)
def learn_topic(payload: LearnRequest):
    topic = payload.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    try:
        article = get_wikipedia_content(topic)
        result = generate_learning_guide(topic=topic, article_text=article["content"], source_title=article["title"])
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # unexpected processing or AI failure
        raise HTTPException(status_code=500, detail=f"Failed to generate guide: {exc}") from exc


@app.post("/explain-simpler", response_model=LearnResponse)
def explain_simpler(payload: LearnRequest):
    topic = payload.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")

    try:
        article = get_wikipedia_content(topic)
        result = simplify_existing_guide(topic=topic, article_text=article["content"], source_title=article["title"])
        return result
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to simplify guide: {exc}") from exc
