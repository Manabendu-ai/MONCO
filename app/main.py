from fastapi import FastAPI

from app.routes.predict import router as prediction_router

app = FastAPI(
    title="MONCO API",
    version="1.1.0"
)

app.include_router(prediction_router)


@app.get("/")
def home():
    return {
        "message": "MONCO Brain Tumor Detection API"
    }