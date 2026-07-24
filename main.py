"""FlyRank W2 · A1 — Task API (Stage 2: read endpoints)."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Task API")

tasks = [
    {"id": 1, "title": "Draft SEO report outline for client onboarding", "done": False},
    {"id": 2, "title": "Review Crawl API response schemas", "done": True},
    {"id": 3, "title": "Ship Week 2 CRUD checkpoint curls", "done": False},
]


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


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )
