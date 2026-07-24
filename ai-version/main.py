"""
AI-generated Task API — first pass from PROMPT_v1.md
Quarantined for Stage 7 rematch. Not the submission.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API")

tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Write tests", "done": False},
    {"id": 3, "title": "Ship MVP", "done": True},
]
next_id = 4


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


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
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    global next_id
    if not payload.title.strip():
        raise HTTPException(status_code=400, detail="title cannot be empty")
    task = {"id": next_id, "title": payload.title, "done": False}
    next_id += 1
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if payload.title is not None:
                task["title"] = payload.title
            if payload.done is not None:
                task["done"] = payload.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
