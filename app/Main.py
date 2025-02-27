from fastapi import FastAPI, Depends, HTTPException
from .db import get_db
from .crud import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    delete_all_tasks
)
from .schemas import TaskCreate, TaskResponse

app = FastAPI(debug=True)

@app.post("/tasks/create_task", response_model=TaskResponse)
def create_task_route(task_data: TaskCreate, db=Depends(get_db)):
    return create_task(db, task_data)

@app.get("/tasks/get_all_tasks", response_model=list[TaskResponse])
def read_tasks(db=Depends(get_db)):
    return get_tasks(db)

@app.get("/tasks/get_task_by_id/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db=Depends(get_db)):
    db_task = get_task_by_id(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена!")
    return db_task

@app.put("/tasks/update_task_by_id/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, task_data: TaskCreate, db=Depends(get_db)):
    updated_task = update_task(db, task_id, task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Задача не найдена!")
    return updated_task

@app.delete("/tasks/delete_task_by_id/{task_id}", response_model=TaskResponse)
def delete_task_route(task_id: int, db=Depends(get_db)):
    deleted_task = delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Задача не найдена!")
    return deleted_task
@app.delete("/tasks/delete_all_tasks")
def delete_all_tasks_route(db=Depends(get_db)):
    return delete_all_tasks(db)