"""FastAPI application entrypoint.

Run locally:   uv run uvicorn ai_ta_api.main:app --reload
In a container: uvicorn ai_ta_api.main:app --host 0.0.0.0 --port 8000
"""

import os

from fastapi import FastAPI

app = FastAPI(title="AI-TA API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness/readiness endpoint. Kubernetes polls this to decide if the pod is healthy.

    APP_ENV is set per environment (local, dev, prod) so we can see which config a pod is
    running; changing it is how we'll demonstrate a rolling update.
    """
    return {"status": "ok", "env": os.getenv("APP_ENV", "local"), "version": app.version}
