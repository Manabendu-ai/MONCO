from ollama import chat

from app.llm.prompt_builder import build_explanation_prompt


class LLMService:
    def __init__(self, model: str = "gemma3:4b"):
        self.model = model

    def generate_explanation(
        self,
        prediction: str,
        confidence: float,
        probabilities: dict,
    ) -> str:

        prompt = build_explanation_prompt(
            prediction=prediction,
            confidence=confidence,
            probabilities=probabilities,
        )

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.message.content.strip()