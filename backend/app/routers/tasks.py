from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database, schemas
from app.routers.auth import get_current_user

import redis.asyncio as redis
import asyncio

r = redis.Redis()

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/ping")
async def ping_tasks():
    return {"message": "Tasks service is alive"}

@router.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authorized!"}

@router.post("/", response_model=schemas.TaskResponse)
async def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_task = models.Task(content=task.content, owner_id=current_user.id)
    db.add(new_task)

    # Commit in thread-safe way for async route
    await asyncio.to_thread(db.commit)
    await asyncio.to_thread(db.refresh, new_task)

    # Broadcast new task
    await r.publish("task_feed", f"{current_user.username}: {task.content}")

    return new_task

@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: str, task: schemas.TaskCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    db_task.content = task.content
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not db_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
