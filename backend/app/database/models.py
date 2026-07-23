from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    image_path = Column(String(500), nullable=False)

    prediction = Column(String(100))

    confidence = Column(Float)

    glioma_probability = Column(Float)

    meningioma_probability = Column(Float)

    pituitary_probability = Column(Float)

    notumor_probability = Column(Float)

    llm_explanation = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
