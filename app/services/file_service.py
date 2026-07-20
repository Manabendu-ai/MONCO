import os
import uuid

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


class FileService:

    @staticmethod
    def save_image(file_bytes: bytes, extension: str):

        filename = f"{uuid.uuid4()}.{extension}"

        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as f:
            f.write(file_bytes)

        return path