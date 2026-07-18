from fastapi import APIRouter, UploadFile, File

from app.services.prediction_service import PredictionService

router = APIRouter(tags=["Prediction"])

prediction_service = PredictionService()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_bytes = await file.read()

    return prediction_service.predict(image_bytes)