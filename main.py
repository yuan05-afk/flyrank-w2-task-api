"""FlyRank W2 · A1 — Task API (Stage 1: root + health)."""

from fastapi import FastAPI

app = FastAPI(title="Task API")


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health")
def health():
    return {"status": "ok"}
