from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..deps import get_current_admin

router = APIRouter(prefix="/api/stats", tags=["Stats"])


@router.get("/")
def get_stats(
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    """Admin-only summary counts used by the dashboard overview page."""
    return {
        "total_images": db.query(models.GalleryImage).count(),
        "active_announcements": db.query(models.Announcement)
        .filter(models.Announcement.is_active.is_(True))
        .count(),
        "total_testimonials": db.query(models.Testimonial).count(),
        "total_messages": db.query(models.Comment).count(),
        "unread_messages": db.query(models.Comment).filter(models.Comment.is_read.is_(False)).count(),
    }
