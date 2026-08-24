import os

from huggingface_hub import InferenceClient

from app.llm.prompt_builder import build_explanation_prompt


class LLMService:

    def __init__(
        self,
        model: str = "deepseek-ai/DeepSeek-V4-Flash-0731:baseten",
    ):
        self.model = model

        self.client = InferenceClient(
            api_key=os.getenv("HF_TOKEN"),
        )

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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are MONCO AI. "
                        "Follow the user's instructions carefully. "
                        "Return only the requested Markdown response."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=400,
        )

        return response.choices[0].message.content.strip()