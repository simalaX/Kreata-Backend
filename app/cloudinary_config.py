"""
Configures the Cloudinary SDK using credentials from settings.
Importing this module applies the configuration as a side effect.
"""
import cloudinary

from .config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)
