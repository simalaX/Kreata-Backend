from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_admin

router = APIRouter(prefix="/api/comments", tags=["Comments"])


@router.post("/", response_model=schemas.CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(payload: schemas.CommentCreate, db: Session = Depends(get_db)):
    """Public endpoint - any website visitor can leave a message. Only the admin can read them."""
    comment = models.Comment(**payload.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=List[schemas.CommentOut])
def list_comments(
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    """Admin-only. Returns every message submitted through the website, newest first."""
    return db.query(models.Comment).order_by(models.Comment.created_at.desc()).all()


@router.patch("/{comment_id}/read", response_model=schemas.CommentOut)
def mark_comment_read(
    comment_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Message not found")
    comment.is_read = True
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(comment)
    db.commit()
    return None
