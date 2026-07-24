"""Central configuration for the MONCO frontend.

Keeping constants here means the API endpoint, class labels, colors, and
emojis can be changed in one place without touching UI or logic code.
"""

BACKEND_BASE_URL = "http://localhost:8000"
API_URL = f"{BACKEND_BASE_URL}/predict"
HISTORY_API_URL = f"{BACKEND_BASE_URL}/history"
REQUEST_TIMEOUT = 30  # seconds
HISTORY_PAGE_SIZE = 12

# Metadata per prediction class: display label, emoji badge, and accent color.
# Add new classes here if the model is retrained with more categories.
CLASS_META = {
    "notumor": {"label": "No Tumor", "emoji": "🟢", "color": "#4ade80"},
    "glioma": {"label": "Glioma", "emoji": "🔴", "color": "#f87171"},
    "meningioma": {"label": "Meningioma", "emoji": "🟡", "color": "#facc15"},
    "pituitary": {"label": "Pituitary", "emoji": "🔵", "color": "#60a5fa"},
}

DEFAULT_CLASS_META = {"label": "Unknown", "emoji": "⚪", "color": "#94a3b8"}


def get_class_meta(class_name: str) -> dict:
    """Look up display metadata for a predicted class name, case-insensitively."""
    return CLASS_META.get(str(class_name).strip().lower(), DEFAULT_CLASS_META)
