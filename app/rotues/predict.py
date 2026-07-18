from io import BytesIO

from fastapi import APIRouter, File, UploadFile
from PIL import Image

from app.services.prediction_service import PredictionService

router = APIRouter()

prediction_service = PredictionService()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_bytes = await file.read()

    image = Image.open(BytesIO(image_bytes))

    result = prediction_service.predict(image)

    return result