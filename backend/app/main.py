import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.database import Base, engine
from app.database import models  # noqa: F401  (ensures models are registered before create_all)
from app.routes.predict import router as prediction_router
from app.routes.history import router as history_router

app = FastAPI(
    title="MONCO API",
    version="1.2.0",
)

# Create MySQL tables (users, prediction_history) if they don't exist yet.
Base.metadata.create_all(bind=engine)

# Serve saved MRI uploads so the frontend can render past scans from history.
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(prediction_router)
app.include_router(history_router)


@app.get("/")
def home():
    return {
        "message": "MONCO Brain Tumor Detection API"
    }
