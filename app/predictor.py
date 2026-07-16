from tensorflow import keras

model = keras.models.load_model("model/monco.keras")

CLASS_NAMES = [
    "glioma",
    "meningioma",
    "notumor",
    "pituitary"
]