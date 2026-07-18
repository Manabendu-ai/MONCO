def build_explanation_prompt(
    prediction: str,
    confidence: float,
    probabilities: dict
) -> str:
    """
    Builds a prompt for the LLM to explain the CNN prediction.
    """

    probability_text = "\n".join(
        [f"- {label}: {score:.2f}%" for label, score in probabilities.items()]
    )

    prompt = f"""
You are an AI medical assistant.

A deep learning model has analyzed a brain MRI image.

Prediction:
{prediction}

Confidence:
{confidence:.2f}%

Class Probabilities:
{probability_text}

Your task:

1. Explain what the predicted class generally means.
2. Explain what the confidence score indicates.
3. Mention that this is an AI-generated prediction.
4. Clearly state that this is NOT a medical diagnosis.
5. Recommend consulting a qualified neurologist or radiologist.
6. Keep the explanation under 150 words.
7. Do NOT invent MRI findings.
8. Do NOT mention tumors other than the predicted class unless necessary.
9. Use simple language understandable by a patient.

Return only the explanation.
"""

    return prompt.strip()