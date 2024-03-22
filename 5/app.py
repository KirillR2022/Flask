from fastapi import FastAPI, HTTPException, Path
from typing import List
from pydantic import BaseModel
from model import Task, TaskCreate

app = FastAPI()

tasks = []

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    task_dict = task.dict()
    task_dict["id"] = len(tasks) + 1
    tasks.append(task_dict)
    return task_dict

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int = Path(..., title="The ID of the task to read")):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskCreate):
    task_to_update = next((task for task in tasks if task["id"] == task_id), None)
    if task_to_update is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_to_update.update(task.dict())
    return task_to_update

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return {"message": "Task deleted successfully"}
