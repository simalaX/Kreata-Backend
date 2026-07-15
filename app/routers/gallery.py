from typing import List, Optional
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import cloudinary_config  # noqa: F401
from .. import models, schemas
from ..database import get_db
from ..deps import get_current_admin

router = APIRouter(prefix="/api/gallery", tags=["Gallery"])

@router.get("/", response_model=List[schemas.GalleryImageOut])
def list_gallery(db: Session = Depends(get_db)):
    """Public endpoint - anyone can view the gallery."""
    return db.query(models.GalleryImage).order_by(models.GalleryImage.created_at.desc()).all()

@router.post("/", response_model=schemas.GalleryImageOut, status_code=status.HTTP_201_CREATED)
async def upload_gallery_image(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    """Admin-only. Uploads an image to Cloudinary and stores its details + description."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    try:
        file_content = await file.read()
        result = cloudinary.uploader.upload(file_content, folder="kreatadesigns/gallery")
    except Exception as exc:
        print(f"Cloudinary upload error: {exc}")  # Log for debugging
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(exc)}")

    new_image = models.GalleryImage(
        title=title,
        description=description,
        category=category,
        image_url=result.get("secure_url"),
        public_id=result.get("public_id"),
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gallery_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    image = db.query(models.GalleryImage).filter(models.GalleryImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        cloudinary.uploader.destroy(image.public_id)
    except Exception:
        pass

    db.delete(image)
    db.commit()
    return None