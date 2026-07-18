"""All communication with the MONCO backend lives here.

Keeping this isolated means the UI never has to know about requests,
timeouts, or JSON parsing - it just calls predict() and gets back either
a result dict or a PredictionError with a friendly message.
"""

import requests

from config import API_URL, REQUEST_TIMEOUT

REQUIRED_KEYS = {"prediction", "confidence", "probabilities"}


class PredictionError(Exception):
    """Raised for any expected, user-facing failure while calling the backend."""


def predict(file_name: str, file_bytes: bytes, file_type: str) -> dict:
    """Send an image to the backend /predict endpoint and return the parsed result.

    Raises PredictionError with a friendly message on any failure - the caller
    never needs to deal with raw exceptions from requests or JSON parsing.
    """
    files = {"file": (file_name, file_bytes, file_type)}

    try:
        response = requests.post(API_URL, files=files, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise PredictionError(
            "The server took too long to respond. Please try again."
        )
    except requests.exceptions.ConnectionError:
        raise PredictionError(
            "Could not reach the MONCO backend. Make sure the API server is running."
        )
    except requests.exceptions.RequestException as exc:
        raise PredictionError(f"Request failed: {exc}")

    if response.status_code != 200:
        raise PredictionError(
            f"Backend returned an error (status {response.status_code})."
        )

    try:
        data = response.json()
    except ValueError:
        raise PredictionError("The backend returned an unreadable response.")

    if not REQUIRED_KEYS.issubset(data.keys()):
        raise PredictionError("The backend response is missing expected fields.")

    return data
