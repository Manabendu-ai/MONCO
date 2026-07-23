from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.history_service import HistoryService

router = APIRouter(prefix="/history", tags=["History"])


@router.get("")
def list_history(
    user_id: Optional[int] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    records = HistoryService.get_history(
        db=db, user_id=user_id, limit=limit, offset=offset
    )

    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "image_path": r.image_path,
            "prediction": r.prediction,
            "confidence": r.confidence,
            "probabilities": {
                "glioma": r.glioma_probability,
                "meningioma": r.meningioma_probability,
                "pituitary": r.pituitary_probability,
                "notumor": r.notumor_probability,
            },
            "explanation": r.llm_explanation,
            "created_at": r.created_at,
        }
        for r in records
    ]


@router.get("/{history_id}")
def get_history_item(history_id: int, db: Session = Depends(get_db)):
    record = HistoryService.get_by_id(db, history_id)

    if record is None:
        raise HTTPException(status_code=404, detail="History record not found")

    return {
        "id": record.id,
        "user_id": record.user_id,
        "image_path": record.image_path,
        "prediction": record.prediction,
        "confidence": record.confidence,
        "probabilities": {
            "glioma": record.glioma_probability,
            "meningioma": record.meningioma_probability,
            "pituitary": record.pituitary_probability,
            "notumor": record.notumor_probability,
        },
        "explanation": record.llm_explanation,
        "created_at": record.created_at,
    }


@router.delete("/{history_id}")
def delete_history_item(history_id: int, db: Session = Depends(get_db)):
    deleted = HistoryService.delete_by_id(db, history_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="History record not found")

    return {"message": "History record deleted"}