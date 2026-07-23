from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.prediction_service import PredictionService

router = APIRouter(tags=["Prediction"])

prediction_service = PredictionService()


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):

    image_bytes = await file.read()

    return prediction_service.predict(
        image_bytes=image_bytes,
        db=db,
        original_filename=file.filename or "",
        user_id=user_id,
    )
