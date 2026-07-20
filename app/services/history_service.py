from sqlalchemy.orm import Session

from app.database.models import PredictionHistory


class HistoryService:

    @staticmethod
    def save_prediction(
        db: Session,
        user_id: int,
        image_path: str,
        prediction: str,
        confidence: float,
        probabilities: dict,
        llm_explanation: str,
    ):

        history = PredictionHistory(

            user_id=user_id,

            image_path=image_path,

            prediction=prediction,

            confidence=confidence,

            glioma_probability=probabilities.get("glioma", 0),

            meningioma_probability=probabilities.get("meningioma", 0),

            pituitary_probability=probabilities.get("pituitary", 0),

            notumor_probability=probabilities.get("notumor", 0),

            llm_explanation=llm_explanation,
        )

        db.add(history)

        db.commit()

        db.refresh(history)

        return history