"""FlyRank W2 · A1 — Task API (Stage 0: hello server)."""

from fastapi import FastAPI

app = FastAPI(title="Task API")


@app.get("/")
def root():
    return {"message": "Hello from the Task API — doors are open."}
