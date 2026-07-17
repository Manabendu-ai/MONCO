import streamlit as st
import requests
from PIL import Image

API_URL = "https://monco-2.onrender.com/predict"

st.set_page_config(
    page_title="MONCO",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        .stApp {
            background: #0f172a;
        }

        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header[data-testid="stHeader"] { background: transparent; }

        .block-container {
            padding-top: 2.5rem;
            max-width: 720px;
        }

        .monco-title {
            font-size: 2.4rem;
            font-weight: 700;
            color: #f1f5f9;
            text-align: center;
            margin-bottom: 0.1rem;
            letter-spacing: 0.03em;
        }
        .monco-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        [data-testid="stFileUploader"] {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 0.6rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #1e293b;
            border: 1px solid #334155 !important;
            border-radius: 12px;
        }

        div.stButton > button {
            width: 100%;
            min-height: 2.8rem;
            background: #2563eb;
            color: white;
            font-weight: 600;
            font-size: 0.95rem;
            line-height: 1.2;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            border: none;
            white-space: nowrap;
        }
        div.stButton > button p {
            font-size: 0.95rem;
            white-space: nowrap;
        }
        div.stButton > button:hover {
            background: #1d4ed8;
            color: white;
        }

        .monco-footer {
            text-align: center;
            color: #64748b;
            font-size: 0.85rem;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid #1e293b;
        }

        .result-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94a3b8;
            margin-bottom: 0.2rem;
        }
        .result-value {
            font-size: 1.4rem;
            font-weight: 700;
        }
        .result-tumor { color: #f87171; }
        .result-clear { color: #4ade80; }

        .confidence-label {
            color: #cbd5e1;
            font-size: 0.9rem;
            margin: 0.8rem 0 0.3rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("### About MONCO")
    st.write(
        "MONCO analyzes MRI brain scans and flags potential tumor regions "
        "using a trained deep learning model."
    )
    st.markdown("---")
    st.markdown("**How to use**")
    st.markdown(
        "1. Upload an MRI scan (JPG/PNG)\n"
        "2. Click Predict\n"
        "3. Review the result and confidence score"
    )
    st.markdown("---")
    st.caption("For research and educational use only. Not a substitute for professional medical diagnosis.")
    st.markdown("---")
    st.caption("Owner: Manabendu Karfa")

st.markdown('<div class="monco-title">MONCO</div>', unsafe_allow_html=True)
st.markdown('<div class="monco-subtitle">AI-Powered Brain Tumor Detection</div>', unsafe_allow_html=True)

predict_clicked = False

with st.container(border=True):
    uploaded_file = st.file_uploader("Upload MRI Scan", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image, caption="Uploaded MRI", width=240)

        predict_clicked = st.button("Predict")

if uploaded_file and predict_clicked:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    with st.spinner("Analyzing scan..."):
        try:
            response = requests.post(API_URL, files=files, timeout=30)
        except requests.exceptions.RequestException:
            response = None

    with st.container(border=True):
        if response is not None and response.status_code == 200:
            data = response.json()
            prediction = str(data.get("prediction", "Unknown"))
            confidence = data.get("confidence", 0)

            is_clear = any(word in prediction.lower() for word in ["no", "clear", "normal"])
            value_class = "result-clear" if is_clear else "result-tumor"

            st.markdown('<div class="result-label">Prediction</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-value {value_class}">{prediction}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="confidence-label">Confidence: {confidence}%</div>', unsafe_allow_html=True)
            st.progress(min(int(confidence), 100) / 100)

        else:
            st.error("Prediction failed. Please check that the API server is running.")


st.markdown('<div class="monco-footer">Owner: Manabendu Karfa</div>', unsafe_allow_html=True)