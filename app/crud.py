from sqlalchemy.orm import Session
from .models import Task

def create_task(db: Session, task_data: dict):
    new_task = Task(Task=task_data.Task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session):
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_data: dict):
    task = get_task_by_id(db, task_id)
    if not task:
        return None
    task.Task = task_data.Task
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task