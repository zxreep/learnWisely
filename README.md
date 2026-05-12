# LearnWisely API (FastAPI + Wikipedia + NVIDIA AI)

Beginner-friendly educational API that takes a topic, pulls Wikipedia content, and returns a clean learning guide in JSON.

## Features
- `POST /learn` beginner-friendly guide
- `POST /explain-simpler` extra simplified version
- `GET /suggestions?q=...` topic suggestions from Wikipedia
- `GET /` health check
- LRU caching for Wikipedia requests
- Clean JSON enforcement for AI output

## Project Structure
```
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
   Then set your `NVIDIA_API_KEY`.

## Run locally
```bash
uvicorn main:app --reload
```

## API Examples
### Health
```bash
curl http://127.0.0.1:8000/
```

### Learn
```bash
curl -X POST http://127.0.0.1:8000/learn \
  -H "Content-Type: application/json" \
  -d '{"topic":"Blockchain"}'
```

### Explain simpler
```bash
curl -X POST http://127.0.0.1:8000/explain-simpler \
  -H "Content-Type: application/json" \
  -d '{"topic":"Photosynthesis"}'
```

## Render Deployment (Free Plan)
1. Push this repo to GitHub.
2. Create a new **Web Service** on Render.
3. Render detects `render.yaml` automatically, or configure manually:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Set environment variable:
   - `NVIDIA_API_KEY`
5. Deploy.

## Response shape (`POST /learn`)
```json
{
  "title": "",
  "simple_explanation": "",
  "learning_roadmap": [""],
  "analogy": "",
  "quiz": [
    {"question": "", "answer": ""}
  ]
}
```
