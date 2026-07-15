"""
Pydantic schemas used for request validation and response serialization.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------------- Auth ----------------

class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AdminOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: Optional[str] = None


# ---------------- Gallery ----------------

class GalleryImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: str
    created_at: datetime


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
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


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
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ---------------- Comments ----------------

class CommentCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: str


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    message: str
    is_read: bool
    created_at: datetime
