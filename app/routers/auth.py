from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db
from ..deps import get_current_admin

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == credentials.username).first()
    if not admin or not security.verify_password(credentials.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = security.create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.AdminOut)
def read_admin_me(current_admin: models.Admin = Depends(get_current_admin)):
    return current_admin


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin),
):
    """Admin-only endpoint to change password."""
    # Verify current password is correct
    if not security.verify_password(request.current_password, current_admin.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Update password
    current_admin.hashed_password = security.hash_password(request.new_password)
    db.add(current_admin)
    db.commit()

    return {"message": "Password changed successfully"}