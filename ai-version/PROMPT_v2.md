# AI rematch — improved prompt (v2)

Build a Python 3.10+ FastAPI Task API in one `main.py` file.

Storage: in-memory Python list only. No database, no files, no Redis.

Seed exactly 3 tasks: each has integer `id`, string `title`, boolean `done`.

Endpoints and status codes:
1. GET `/` → 200 `{"name":"Task API","version":"1.0","endpoints":["/tasks"]}`
2. GET `/health` → 200 `{"status":"ok"}`
3. GET `/tasks` → 200 array of tasks
4. GET `/tasks/{id}` → 200 task OR 404 body exactly `{"error":"Task {id} not found"}` (top-level `error`, not FastAPI `detail`)
5. POST `/tasks` body `{"title":"..."}` → 201 created task with next free id and `done: false`. Missing/empty/whitespace title → 400 `{"error":"..."}` (must be 400, not 422)
6. PUT `/tasks/{id}` body may include `title` and/or `done`. Unknown id → 404 same error shape. Empty `{}` or invalid title/done → 400
7. DELETE `/tasks/{id}` → 204 with empty body on success; 404 with `{"error":"..."}` if missing

Also: FastAPI Swagger at `/docs`. Map validation failures to HTTP 400 JSON errors with an `error` key.
Do not add authentication, CORS, or a database.
