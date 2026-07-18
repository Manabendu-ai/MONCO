from PIL import Image

from app.model.predictor import Predictor
from app.llm.service import LLMService


class PredictionService:

    def __init__(self):
        self.predictor = Predictor()
        self.llm = LLMService()

    def predict(self, image: Image.Image):

        # CNN Prediction
        prediction_result = self.predictor.predict(image)

        # LLM Explanation
        explanation = self.llm.generate_explanation(
            prediction=prediction_result["prediction"],
            confidence=prediction_result["confidence"],
            probabilities=prediction_result["probabilities"],
        )

        prediction_result["explanation"] = explanation

        return prediction_result