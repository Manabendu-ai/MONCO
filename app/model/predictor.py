import numpy as np
from PIL import Image

from app.model.loader import model, CLASS_NAMES


class Predictor:
    def __init__(self):
        self.model = model
        self.class_names = CLASS_NAMES

    def preprocess(self, image: Image.Image):
        """
        Preprocess the uploaded image before inference.
        """

        image = image.convert("RGB")
        image = image.resize((128, 128))

        image = np.array(image, dtype=np.float32)
        image = image / 255.0

        image = np.expand_dims(image, axis=0)

        return image

    def predict(self, image: Image.Image):

        image = self.preprocess(image)

        predictions = self.model.predict(image, verbose=0)[0]

        predicted_index = np.argmax(predictions)

        predicted_class = self.class_names[predicted_index]

        confidence = float(predictions[predicted_index] * 100)

        probabilities = {
            self.class_names[i]: float(predictions[i] * 100)
            for i in range(len(self.class_names))
        }

        return {
            "prediction": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": probabilities
        }