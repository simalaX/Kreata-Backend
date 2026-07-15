"""
SQLAlchemy ORM models with type hints for SQLAlchemy 2.0.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func

from .database import Base


class Admin(Base):
    __tablename__ = "admins"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(50), unique=True, index=True, nullable=False)
    email: str = Column(String(120), unique=True, nullable=True)
    hashed_password: str = Column(String(255), nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now())


class GalleryImage(Base):
    __tablename__ = "gallery_images"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(150), nullable=False)
    description: str = Column(Text, nullable=True)
    category: str = Column(String(100), nullable=True)
    image_url: str = Column(String(500), nullable=False)
    public_id: str = Column(String(255), nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now())


class Announcement(Base):
    __tablename__ = "announcements"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(200), nullable=False)
    message: str = Column(Text, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now())


class Testimonial(Base):
    __tablename__ = "testimonials"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(150), nullable=False)
    message: str = Column(Text, nullable=False)
    rating: int = Column(Integer, default=5, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now())


class Comment(Base):
    """User-submitted feedback / enquiries from the public website.
    Only visible to the admin via the dashboard - not displayed publicly."""
    __tablename__ = "comments"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(150), nullable=False)
    email: str = Column(String(150), nullable=True)
    phone: str = Column(String(30), nullable=True)
    message: str = Column(Text, nullable=False)
    is_read: bool = Column(Boolean, default=False, nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now())