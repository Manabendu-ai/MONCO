from app.llm.service import LLMService

service = LLMService()

result = service.generate_explanation(
    prediction="Glioma",
    confidence=97.42,
    probabilities={
        "Glioma": 97.42,
        "Pituitary": 1.21,
        "Meningioma": 0.82,
        "No Tumor": 0.55,
    },
)

print(result)