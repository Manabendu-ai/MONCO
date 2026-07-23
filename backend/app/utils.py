import numpy as np
from tensorflow.keras.utils import load_img
from PIL import Image
import io

IMAGE_SIZE = 128

def preprocess_image(contents):

    image = Image.open(io.BytesIO(contents))
    image = image.convert("RGB")
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))

    image = np.array(image) / 255.0

    image = np.expand_dims(image, axis=0)

    return image