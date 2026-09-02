# AI-TA

A small, working rebuild of an AI teaching-assistant platform, written from scratch as a personal
learning project. It ingests course files, answers student questions with retrieval-augmented
generation (RAG), refuses to hand over assignment answers, generates quizzes, and talks out loud.

## Architecture

```
                         ┌──────────────┐
                         │   apps/web   │  React + Vite
                         └──────┬───────┘
                                │ REST (JSON)
                         ┌──────▼───────┐
                         │ services/api │  FastAPI
                         │  /chat /quiz │
                         │  /auth /health
                         └──┬───┬───┬───┘
                            │   │   │
        ┌───────────────────┘   │   └─────────────────────┐
        ▼                       ▼                         ▼
  ┌───────────┐          ┌────────────┐            ┌────────────┐
  │  MongoDB  │          │   Neo4j    │            │  Pinecone  │
  │ users     │          │ Class      │            │ vectors +  │
  │ convos    │          │  └►Topic   │            │ metadata   │
  │ documents │          │     └►Doc  │            └─────▲──────┘
  └───────────┘          └────────────┘                  │
                                                          │ upsert
                    ┌────────────────┐    ┌───────────────┴──────┐
   course files ───►│ services/worker│───►│ packages/ingest      │
                    │ (ingest runner)│    │ source → extract →   │
                    └────────────────┘    │ chunk → embed → sink │
                                          └──────────────────────┘

  LLM calls (chat, anti-cheating check, quiz, topic extraction) go through one `LLMClient`
  interface: OpenAI now, Claude on Amazon Bedrock after the AWS deployment.
```

Request flow for a chat message: embed the question → ask Neo4j which documents belong to this
class and topic → query Pinecone filtered to those documents → anti-cheating classifier → generate
an answer from the retrieved context → persist the turn to MongoDB → return answer + sources.

## Layout

| Path                 | What lives there                                   |
| -------------------- | -------------------------------------------------- |
| `apps/web/`          | React frontend (Vite + TypeScript)                 |
| `services/api/`      | FastAPI service: chat, quiz, auth, conversations   |
| `services/worker/`   | Ingest runner that executes pipeline manifests     |
| `packages/ingest/`   | Ingest operators + manifest loader (shared code)   |
| `k8s/`               | Kubernetes manifests                               |
| `.github/workflows/` | CI/CD                                              |
| `docs/`              | Interview notes and design notes                   |

## Local setup

```powershell
uv sync                      # create .venv with Python 3.12 and install dependencies
Copy-Item .env.example .env  # then fill in your keys
uv run pytest                # run tests
uv run ruff check .          # lint
```

Runs on Windows with PowerShell, Docker Desktop (WSL 2), and `uv`.
