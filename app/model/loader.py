from tensorflow import keras
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model = keras.models.load_model(BASE_DIR / "model" / "monco.keras")

with open(BASE_DIR / "model" / "classes.json") as f:
    CLASS_NAMES = json.load(f)