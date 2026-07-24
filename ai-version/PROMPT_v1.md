# AI rematch — first prompt (written from memory, not copied from the brief)

Build a Python FastAPI to-do API that stores tasks only in a Python list in memory (no database).

Requirements:
- Run on port 8000
- GET / returns {"name":"Task API","version":"1.0","endpoints":["/tasks"]}
- GET /health returns {"status":"ok"}
- Seed 3 tasks with id, title, done
- GET /tasks lists all
- GET /tasks/{id} returns one task or 404 {"error":"Task N not found"}
- POST /tasks with {"title":"..."} creates with next id, done=false, status 201
- Missing/empty title on POST → 400 with JSON error
- PUT /tasks/{id} updates title and/or done; 404 if missing; 400 if body invalid/empty
- DELETE /tasks/{id} returns 204 empty body, or 404
- Swagger UI available (FastAPI default /docs)
- Put everything in one main.py file with requirements.txt

Keep it simple. One file is fine.
