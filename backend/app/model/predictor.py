import numpy as np

from app.model.loader import model, CLASS_NAMES
from app.utils import preprocess_image


class Predictor:

    def __init__(self):
        self.model = model
        self.class_names = CLASS_NAMES

    def predict(self, image_bytes: bytes):

        image = preprocess_image(image_bytes)

        predictions = self.model.predict(image, verbose=0)[0]

        predicted_index = int(np.argmax(predictions))

        predicted_class = self.class_names[predicted_index]

        confidence = float(predictions[predicted_index] * 100)

        probabilities = {
            self.class_names[i]: round(float(predictions[i] * 100), 2)
            for i in range(len(self.class_names))
        }

        return {
            "prediction": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": probabilities,
        }