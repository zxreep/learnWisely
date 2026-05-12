# LearnWisely API (FastAPI + Wikipedia + NVIDIA AI) - Learning Framework Edition

Beginner-friendly educational API that takes a topic, pulls Wikipedia content, and returns a structured learning framework JSON.

## Features
- `POST /learn` difficulty-aware framework (`overview`, `mediocre`, `expert`)
- `GET /suggestions?q=...` topic suggestions from Wikipedia
- `GET /` health check
- LRU caching for Wikipedia requests
- Clean JSON enforcement for AI output

## Project Structure
```txt
project/
├── main.py
├── scraper.py
├── ai.py
├── prompts.py
├── requirements.txt
├── render.yaml
├── .env.example
└── README.md
```

## Setup
1. Create and activate venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure env:
   ```bash
   cp .env.example .env
   ```
4. Set your `NVIDIA_API_KEY` in `.env`.

## Run locally
```bash
uvicorn main:app --reload
```

## API Examples
### Health
```bash
curl http://127.0.0.1:8000/
```

### Learn framework
```bash
curl -X POST http://127.0.0.1:8000/learn \
  -H "Content-Type: application/json" \
  -d '{"topic":"Blockchain","difficulty":"overview"}'
```

## Render Deployment (Free Plan)
1. Push this repo to GitHub.
2. Create a new **Web Service** on Render.
3. Render uses `render.yaml` automatically, or set manually:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Set environment variable:
   - `NVIDIA_API_KEY`
5. Deploy.

## Response shape (`POST /learn`)
```json
{
  "title": "Blockchain Learning Framework",
  "learner_level": "overview",
  "strategy": "Understand core ideas first, then basic use-cases.",
  "modules": [
    {
      "topic": "Blockchain Basics",
      "summary": "What blockchain is and why it exists.",
      "subtopics": [
        {"name": "Blocks and chains", "objective": "Understand structure", "estimated_hours": 2}
      ]
    }
  ],
  "final_project": "Create a beginner presentation comparing blockchain vs regular databases.",
  "quiz": [
    {"question": "What is a block?", "answer": "A container of verified records."}
  ]
}
```
