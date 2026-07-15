"""
Application configuration.
All values are read from environment variables (or a local .env file).
See .env.example for the full list of variables you need to set.
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT auth
    SECRET_KEY: str = "Yw9vIe0kTYCEW2U46GQXFbZ7UI5FUmwWG/QXmlG/O86if5GNhsCnmcHQiyG9VSdUbSqL4Y8MPUEf6sJcwJeooA=="
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Default admin account (auto-created on first startup if it doesn't exist)
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "change-this-password"
    ADMIN_EMAIL: str = "admin@kreatadesigns.com"

    # Cloudinary (image storage)
    CLOUDINARY_CLOUD_NAME: str = "maklffcg"
    CLOUDINARY_API_KEY: str = "939425629812264"
    CLOUDINARY_API_SECRET: str = "WGBHv9jC86a09z4bM8yjuz3pGk8"

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()