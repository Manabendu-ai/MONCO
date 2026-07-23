import os
import uuid

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


class FileService:

    @staticmethod
    def save_image(file_bytes: bytes, original_filename: str = "") -> str:
        """Saves the uploaded MRI image to disk with a unique name and
        returns the relative path (stored in the DB as image_path)."""

        extension = ""
        if original_filename and "." in original_filename:
            extension = original_filename.rsplit(".", 1)[-1].lower()

        if not extension:
            extension = "jpg"

        filename = f"{uuid.uuid4()}.{extension}"

        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as f:
            f.write(file_bytes)

        return path
