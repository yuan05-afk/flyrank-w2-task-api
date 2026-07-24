"""
AI-generated Task API — rematch from PROMPT_v2.md
Still quarantined. Closer on status codes; error shape improved.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

app = FastAPI(title="Task API", version="1.0.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Write tests", "done": False},
    {"id": 3, "title": "Ship MVP", "done": True},
]
next_id = 4


@app.exception_handler(RequestValidationError)
async def validation_handler(_: Request, __: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})


def find(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return task


@app.post("/tasks", status_code=201)
async def create_task(request: Request):
    global next_id
    body = await request.json()
    title = body.get("title") if isinstance(body, dict) else None
    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title is required and must be a non-empty string"},
        )
    task = {"id": next_id, "title": title.strip(), "done": False}
    next_id += 1
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    task = find(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    body = await request.json()
    if not isinstance(body, dict) or not body:
        return JSONResponse(status_code=400, content={"error": "empty or invalid body"})
    if "title" in body:
        if not isinstance(body["title"], str) or not body["title"].strip():
            return JSONResponse(status_code=400, content={"error": "invalid title"})
        task["title"] = body["title"].strip()
    if "done" in body:
        if not isinstance(body["done"], bool):
            return JSONResponse(status_code=400, content={"error": "invalid done"})
        task["done"] = body["done"]
    if "title" not in body and "done" not in body:
        return JSONResponse(status_code=400, content={"error": "empty or invalid body"})
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = find(task_id)
    if not task:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    tasks.remove(task)
    return Response(status_code=204)
