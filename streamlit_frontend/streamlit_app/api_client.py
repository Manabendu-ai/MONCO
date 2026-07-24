"""All communication with the MONCO backend lives here.

Keeping this isolated means the UI never has to know about requests,
timeouts, or JSON parsing - it just calls predict() and gets back either
a result dict or a PredictionError with a friendly message.
"""

import requests

from config import API_URL, HISTORY_API_URL, BACKEND_BASE_URL, REQUEST_TIMEOUT

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


def get_history(limit: int = 12, offset: int = 0) -> list:
    """Fetch past predictions from the backend /history endpoint.

    Raises PredictionError with a friendly message on any failure, same as
    predict(), so the UI can handle both the same way.
    """
    params = {"limit": limit, "offset": offset}

    try:
        response = requests.get(HISTORY_API_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise PredictionError("The server took too long to respond. Please try again.")
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
        return response.json()
    except ValueError:
        raise PredictionError("The backend returned an unreadable response.")


def delete_history_item(history_id: int) -> None:
    """Delete a single history record on the backend."""
    try:
        response = requests.delete(
            f"{HISTORY_API_URL}/{history_id}", timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException as exc:
        raise PredictionError(f"Request failed: {exc}")

    if response.status_code != 200:
        raise PredictionError(
            f"Backend returned an error (status {response.status_code})."
        )


def history_image_url(image_path: str) -> str:
    """Build a full URL for an image path returned by the backend

    (e.g. 'uploads/xyz.jpg' -> 'http://localhost:8000/uploads/xyz.jpg').
    """
    return f"{BACKEND_BASE_URL}/{image_path.lstrip('/')}"
