"""
FlyRank Internship · Backend Track · W2 A1
In-memory Task API — full CRUD + Swagger + stretch extras.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

SEED_TASKS: list[dict[str, Any]] = [
    {"id": 1, "title": "Draft SEO report outline for client onboarding", "done": False},
    {"id": 2, "title": "Review Crawl API response schemas", "done": True},
    {"id": 3, "title": "Ship Week 2 CRUD checkpoint curls", "done": False},
]

app = FastAPI(
    title="Task API",
    version="1.0.0",
    description=(
        "FlyRank W2 · A1 — a small in-memory to-do API. "
        "Data lives only in process memory: restart the server and everything resets. "
        "Interactive docs: **/docs**."
    ),
    contact={"name": "FlyRank Backend Intern"},
    license_info={"name": "MIT"},
)

tasks: list[dict[str, Any]] = deepcopy(SEED_TASKS)
next_id: int = 4


class TaskOut(BaseModel):
    id: int
    title: str
    done: bool


class ErrorOut(BaseModel):
    error: str


class StatsOut(BaseModel):
    total: int
    done: int
    open: int


class ApiInfo(BaseModel):
    name: str
    version: str
    endpoints: list[str]


class HealthOut(BaseModel):
    status: str


class ResetOut(BaseModel):
    message: str
    tasks: list[TaskOut]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    """Map FastAPI/Pydantic 422 validation failures to assignment-friendly 400s."""
    errors = exc.errors()
    for err in errors:
        loc = err.get("loc", ())
        field = loc[-1] if loc else None
        if field == "title":
            return JSONResponse(
                status_code=400,
                content={"error": "title is required and must be a non-empty string"},
            )
        if field == "done":
            return JSONResponse(
                status_code=400,
                content={"error": "done must be a boolean"},
            )
    return JSONResponse(status_code=400, content={"error": "Invalid request body"})


def find_task(task_id: int) -> dict[str, Any] | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def not_found(task_id: int) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"},
    )


@app.get(
    "/",
    response_model=ApiInfo,
    tags=["meta"],
    summary="API front door",
    description="Describes this API: name, version, and primary resource paths.",
)
def root() -> dict[str, Any]:
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/stats", "/reset", "/health", "/docs"],
    }


@app.get(
    "/health",
    response_model=HealthOut,
    tags=["meta"],
    summary="Liveness check",
    description="Returns ok when the server process is accepting requests.",
)
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/stats",
    response_model=StatsOut,
    tags=["extras"],
    summary="Task counts",
    description="Computes totals from the in-memory list — no storage beyond RAM.",
)
def stats() -> dict[str, int]:
    done = sum(1 for t in tasks if t["done"])
    total = len(tasks)
    return {"total": total, "done": done, "open": total - done}


@app.post(
    "/reset",
    response_model=ResetOut,
    tags=["extras"],
    summary="Restore seed tasks",
    description="Wipes the list and restores the three example tasks. Handy for demos.",
)
def reset() -> dict[str, Any]:
    global tasks, next_id
    tasks = deepcopy(SEED_TASKS)
    next_id = 4
    return {"message": "Seed tasks restored", "tasks": tasks}


@app.get(
    "/tasks",
    response_model=list[TaskOut],
    tags=["tasks"],
    summary="List tasks",
    description=(
        "Returns tasks from memory. Optional filters: done, search. "
        "Optional pagination: limit + offset (real APIs page results so clients stay fast)."
    ),
    responses={400: {"model": ErrorOut}},
)
def list_tasks(
    done: bool | None = Query(
        None,
        description="If set, only return tasks with this done value.",
    ),
    search: str | None = Query(
        None,
        description="Case-insensitive substring match against title.",
    ),
    limit: int | None = Query(
        None,
        ge=1,
        le=100,
        description="Max number of tasks to return (pagination).",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of matching tasks to skip (pagination).",
    ),
) -> list[dict[str, Any]]:
    results = tasks

    if done is not None:
        results = [t for t in results if t["done"] is done]

    if search is not None and search.strip():
        needle = search.strip().lower()
        results = [t for t in results if needle in t["title"].lower()]

    if offset:
        results = results[offset:]

    if limit is not None:
        results = results[:limit]

    return results


@app.get(
    "/tasks/{task_id}",
    response_model=TaskOut,
    tags=["tasks"],
    summary="Get one task",
    description="Fetch a single task by path id. Unknown ids return 404 with a JSON error.",
    responses={404: {"model": ErrorOut}},
)
def get_task(task_id: int) -> dict[str, Any] | JSONResponse:
    task = find_task(task_id)
    if task is None:
        return not_found(task_id)
    return task


@app.post(
    "/tasks",
    response_model=TaskOut,
    status_code=201,
    tags=["tasks"],
    summary="Create a task",
    description="Creates a task with the next free id and done=false. Empty/missing title → 400.",
    responses={400: {"model": ErrorOut}},
)
async def create_task(request: Request) -> dict[str, Any] | JSONResponse:
    global next_id
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Request body must be JSON"})

    if not isinstance(body, dict):
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be a JSON object"},
        )

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


@app.put(
    "/tasks/{task_id}",
    response_model=TaskOut,
    tags=["tasks"],
    summary="Update a task",
    description="Updates title and/or done. Empty body or invalid fields → 400. Unknown id → 404.",
    responses={400: {"model": ErrorOut}, 404: {"model": ErrorOut}},
)
async def update_task(task_id: int, request: Request) -> dict[str, Any] | JSONResponse:
    task = find_task(task_id)
    if task is None:
        return not_found(task_id)

    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={"error": "Request body must be JSON"})

    if not isinstance(body, dict) or not body:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must include title and/or done"},
        )

    if "title" not in body and "done" not in body:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must include title and/or done"},
        )

    if "title" in body:
        title = body["title"]
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "title must be a non-empty string"},
            )
        task["title"] = title.strip()

    if "done" in body:
        done = body["done"]
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400,
                content={"error": "done must be a boolean"},
            )
        task["done"] = done

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    tags=["tasks"],
    summary="Delete a task",
    description="Removes a task. Success returns 204 with an empty body. Unknown id → 404.",
    response_class=Response,
)
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return not_found(task_id)
    tasks.remove(task)
    return Response(status_code=204)
