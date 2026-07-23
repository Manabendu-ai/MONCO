from typing import Optional

from sqlalchemy.orm import Session

from app.database.models import PredictionHistory


class HistoryService:

    @staticmethod
    def save_prediction(
        db: Session,
        image_path: str,
        prediction: str,
        confidence: float,
        probabilities: dict,
        llm_explanation: str,
        user_id: Optional[int] = None,
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

    @staticmethod
    def get_history(
        db: Session,
        user_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ):
        query = db.query(PredictionHistory)

        if user_id is not None:
            query = query.filter(PredictionHistory.user_id == user_id)

        return (
            query.order_by(PredictionHistory.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, history_id: int):
        return (
            db.query(PredictionHistory)
            .filter(PredictionHistory.id == history_id)
            .first()
        )

    @staticmethod
    def delete_by_id(db: Session, history_id: int) -> bool:
        history = HistoryService.get_by_id(db, history_id)

        if history is None:
            return False

        db.delete(history)
        db.commit()

        return True
