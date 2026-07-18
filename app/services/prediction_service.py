from app.model.predictor import Predictor
from app.llm.service import LLMService


class PredictionService:

    def __init__(self):
        self.predictor = Predictor()
        self.llm = LLMService()

    def predict(self, image_bytes: bytes):

        prediction = self.predictor.predict(image_bytes)

        explanation = self.llm.generate_explanation(
            prediction=prediction["prediction"],
            confidence=prediction["confidence"],
            probabilities=prediction["probabilities"]
        )

        prediction["explanation"] = explanation

        return prediction