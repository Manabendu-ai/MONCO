import os

from groq import Groq

from app.llm.prompt_builder import build_explanation_prompt


class LLMService:

    def __init__(
        self,
        model: str = "openai/gpt-oss-120b",
    ):
        self.model = model

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
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
            temperature=0.4,
            max_completion_tokens=800,
        )

        print("LLM RESPONSE:", response)

        content = response.choices[0].message.content

        print("LLM CONTENT:", content)

        return content.strip() if content else "AI explanation could not be generated."