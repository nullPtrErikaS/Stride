from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, database, schemas
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/reactions",
    tags=["Reactions"]
)

@router.get("/ping")
async def ping_reactions():
    return {"message": "Reactions service is alive"}

@router.post("/", response_model=schemas.ReactionResponse)
def create_reaction(reaction: schemas.ReactionCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Check if the task exists
    task = db.query(models.Task).filter(models.Task.id == reaction.task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

    new_reaction = models.Reaction(
        task_id=reaction.task_id,
        user_id=current_user.id,
        reaction_type=reaction.reaction_type
    )
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    return new_reaction

@router.get("/", response_model=list[schemas.ReactionResponse])
def get_user_reactions(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Reaction).filter(models.Reaction.user_id == current_user.id).all()

@router.delete("/{reaction_id}")
def delete_reaction(reaction_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_reaction = db.query(models.Reaction).filter(models.Reaction.id == reaction_id, models.Reaction.user_id == current_user.id).first()
    if not db_reaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found.")
    db.delete(db_reaction)
    db.commit()
    return {"message": "Reaction deleted successfully"}

@router.post("/{task_id}/like")
def like_task(task_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if already reacted
    reaction = db.query(models.Reaction).filter(
        models.Reaction.task_id == task.id,
        models.Reaction.user_id == current_user.id
    ).first()

    if reaction:
        reaction.reaction_type = "like"
    else:
        reaction = models.Reaction(task_id=task.id, user_id=current_user.id, reaction_type="like")
        db.add(reaction)

    db.commit()
    db.refresh(reaction)
    return {"message": "Task liked successfully"}

@router.post("/{task_id}/dislike")
def dislike_task(task_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Check if already reacted
    reaction = db.query(models.Reaction).filter(
        models.Reaction.task_id == task.id,
        models.Reaction.user_id == current_user.id
    ).first()

    if reaction:
        reaction.reaction_type = "dislike"
    else:
        reaction = models.Reaction(task_id=task.id, user_id=current_user.id, reaction_type="dislike")
        db.add(reaction)

    db.commit()
    db.refresh(reaction)
    return {"message": "Task disliked successfully"}

@router.get("/task/{task_id}/summary")
def reaction_summary(task_id: str, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    likes = db.query(models.Reaction).filter(
        models.Reaction.task_id == task_id,
        models.Reaction.reaction_type == "like"
    ).count()

    dislikes = db.query(models.Reaction).filter(
        models.Reaction.task_id == task_id,
        models.Reaction.reaction_type == "dislike"
    ).count()

    return {
        "task_id": task_id,
        "likes": likes,
        "dislikes": dislikes
    }
