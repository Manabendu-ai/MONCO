from fastapi import FastAPI, UploadFile, File
import numpy as np

from .loader import model, CLASS_NAMES
from .utils import preprocess_image

app = FastAPI(title="MONCO API")


@app.get("/")
def home():
    return {
        "message": "MONCO Brain Tumor Detection API"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()

    image = preprocess_image(contents)

    prediction = model.predict(image)

    index = np.argmax(prediction)

    confidence = float(np.max(prediction))

    return {
        "prediction": CLASS_NAMES[index],
        "confidence": round(confidence * 100, 2)
    }