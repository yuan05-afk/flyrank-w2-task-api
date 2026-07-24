"""FlyRank W2 · A1 — Task API (Stage 3: create with validation)."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Task API")

tasks = [
    {"id": 1, "title": "Draft SEO report outline for client onboarding", "done": False},
    {"id": 2, "title": "Review Crawl API response schemas", "done": True},
    {"id": 3, "title": "Ship Week 2 CRUD checkpoint curls", "done": False},
]
next_id = 4


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    missing_title = any(
        err.get("loc", [])[-1] == "title" and err.get("type") in {"missing", "string_too_short"}
        for err in exc.errors()
    )
    if missing_title:
        message = "title is required and must be a non-empty string"
    else:
        message = "Invalid request body"
    return JSONResponse(status_code=400, content={"error": message})


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


@app.post("/tasks", status_code=201)
async def create_task(request: Request):
    global next_id
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Request body must be JSON"})

    if not isinstance(body, dict):
        return JSONResponse(status_code=400, content={"error": "Request body must be a JSON object"})

    title = body.get("title")
    if title is None or not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title is required and must be a non-empty string"},
        )

    task = {"id": next_id, "title": title.strip(), "done": False}
    next_id += 1
    tasks.append(task)
    return task
