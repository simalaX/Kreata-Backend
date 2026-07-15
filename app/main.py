"""
Kreata Designs API - FastAPI application entrypoint.

Run locally with:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models, security
from .config import settings
from .database import Base, SessionLocal, engine
from .routers import announcements, auth, comments, gallery, stats


def _seed_admin(db):
    """Creates the default admin account from env vars if none exists yet."""
    existing = db.query(models.Admin).filter(models.Admin.username == settings.ADMIN_USERNAME).first()
    if not existing:
        admin = models.Admin(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            hashed_password=security.hash_password(settings.ADMIN_PASSWORD),
        )
        db.add(admin)
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        _seed_admin(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Kreata Designs API", version="1.0.0", lifespan=lifespan)

origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "https://kreatadesigns.com",
    "https://www.kreatadesigns.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(gallery.router)
app.include_router(announcements.router)
app.include_router(comments.router)
app.include_router(stats.router)


@app.get("/")
def root():
    return {"message": "Kreata Designs API is running"}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}