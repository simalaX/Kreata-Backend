"""
Pydantic schemas used for request validation and response serialization.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ---------------- Auth ----------------

class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None

    class Config:
        orm_mode = True


# ---------------- Gallery ----------------

class GalleryImageOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: str
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------- Announcements ----------------

class AnnouncementBase(BaseModel):
    title: str
    message: str
    is_active: bool = True


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    is_active: Optional[bool] = None


class AnnouncementOut(AnnouncementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------- Testimonials ----------------

class TestimonialBase(BaseModel):
    name: str
    message: str
    rating: int = 5
    is_active: bool = True


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    message: Optional[str] = None
    rating: Optional[int] = None
    is_active: Optional[bool] = None


class TestimonialOut(TestimonialBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------- Comments ----------------

class CommentCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: str


class CommentOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True