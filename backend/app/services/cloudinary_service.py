import os
import cloudinary
import cloudinary.uploader
from app.config import cloudinary_config

class CloudinaryService:

    @staticmethod
    def upload_image(
        image_bytes: bytes,
        filename: str = "",
    ) -> str:

        result = cloudinary.uploader.upload(
            image_bytes,
            folder="monco/predictions",
            public_id=os.path.splitext(filename)[0] if filename else None,
            resource_type="image",
        )

        return result["secure_url"]