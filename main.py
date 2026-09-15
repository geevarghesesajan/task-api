from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple in-memory CRUD API for managing tasks."
)

tasks_db = [
    {"id": 1, "title": "Complete Stage 0", "done": True},
    {"id": 2, "title": "Build CRUD endpoints", "done": False},
    {"id": 3, "title": "Submit assignment", "done": False},
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/", summary="Root Endpoint")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/docs"]
    }

@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="List All Tasks")
def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", summary="Get Single Task")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create Task")
def create_task(task_in: TaskCreate):
    if not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {"id": next_id, "title": task_in.title, "done": False}
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{task_id}", summary="Update Task")
def update_task(task_id: int, task_in: TaskUpdate):
    for task in tasks_db:
        if task["id"] == task_id:
            if task_in.title is not None:
                if not task_in.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = task_in.title
            if task_in.done is not None:
                task["done"] = task_in.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Task")
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")