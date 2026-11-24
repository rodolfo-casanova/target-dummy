"""API REST de ejemplo para tareas, hecha con FastAPI. Sin pruebas a propósito."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Target Dummy API")

tasks: dict[int, dict] = {}
next_id = 1


class TaskIn(BaseModel):
    title: str
    done: bool = False


class Task(TaskIn):
    id: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskIn):
    global next_id
    task = {"id": next_id, **payload.model_dump()}
    tasks[next_id] = task
    next_id += 1
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tasks[task_id]


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskIn):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    tasks[task_id] = {"id": task_id, **payload.model_dump()}
    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    del tasks[task_id]
