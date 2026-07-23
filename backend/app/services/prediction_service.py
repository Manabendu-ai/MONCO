from typing import Optional

from sqlalchemy.orm import Session

from app.model.predictor import Predictor
from app.llm.service import LLMService
from app.services.file_service import FileService
from app.services.history_service import HistoryService


class PredictionService:

    def __init__(self):
        self.predictor = Predictor()
        self.llm = LLMService()

    def predict(
        self,
        image_bytes: bytes,
        db: Session,
        original_filename: str = "",
        user_id: Optional[int] = None,
    ):

        prediction = self.predictor.predict(image_bytes)

        explanation = self.llm.generate_explanation(
            prediction=prediction["prediction"],
            confidence=prediction["confidence"],
            probabilities=prediction["probabilities"],
        )

        prediction["explanation"] = explanation

        # Persist the uploaded image + result so it shows up in history.
        image_path = FileService.save_image(image_bytes, original_filename)

        history = HistoryService.save_prediction(
            db=db,
            image_path=image_path,
            prediction=prediction["prediction"],
            confidence=prediction["confidence"],
            probabilities=prediction["probabilities"],
            llm_explanation=explanation,
            user_id=user_id,
        )

        prediction["id"] = history.id
        prediction["image_path"] = image_path
        prediction["created_at"] = history.created_at

        return prediction
