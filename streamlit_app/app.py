import streamlit as st
import requests
from PIL import Image

API_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="MONCO",
    layout="centered"
)

st.title("MONCO")
st.subheader("Brain Tumor Detection")

uploaded_file = st.file_uploader(
    "Upload MRI Scan",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded MRI",
        use_container_width=True
    )

    if st.button("Predict"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        response = requests.post(
            API_URL,
            files=files
        )

        if response.status_code == 200:

            data = response.json()

            st.success(
                f"Prediction : {data['prediction']}"
            )

            st.write(
                f"Confidence : {data['confidence']}%"
            )

        else:

            st.error("Prediction Failed")