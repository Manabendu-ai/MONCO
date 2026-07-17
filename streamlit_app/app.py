import streamlit as st
import requests
from PIL import Image

API_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="MONCO",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Custom styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Overall app background */
        .stApp {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        }

        /* Hide default streamlit chrome */
        #MainMenu, header, footer { visibility: hidden; }

        /* Title block */
        .monco-header {
            text-align: center;
            padding: 1.2rem 0 0.2rem 0;
        }
        .monco-title {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            letter-spacing: 0.05em;
        }
        .monco-subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
            margin-top: 0.2rem;
        }

        /* Card containers */
        .monco-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        }

        /* Uploader tweaks */
        [data-testid="stFileUploader"] {
            background: #1e293b;
            border: 1.5px dashed #475569;
            border-radius: 14px;
            padding: 0.8rem;
        }

        /* Predict button */
        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #38bdf8, #6366f1);
            color: white;
            font-weight: 700;
            font-size: 1rem;
            padding: 0.7rem 0;
            border-radius: 12px;
            border: none;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(56, 189, 248, 0.35);
            color: white;
        }

        /* Result badges */
        .result-box {
            border-radius: 14px;
            padding: 1.1rem 1.4rem;
            font-size: 1.15rem;
            font-weight: 700;
            text-align: center;
            margin-top: 0.6rem;
        }
        .result-tumor {
            background: rgba(248, 113, 113, 0.12);
            border: 1px solid #f87171;
            color: #fca5a5;
        }
        .result-clear {
            background: rgba(74, 222, 128, 0.12);
            border: 1px solid #4ade80;
            color: #86efac;
        }

        .confidence-label {
            color: #cbd5e1;
            font-size: 0.95rem;
            margin-top: 0.6rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧠 About MONCO")
    st.write(
        "MONCO analyzes MRI brain scans and flags potential tumor regions "
        "using a trained deep learning model."
    )
    st.markdown("---")
    st.markdown("**How to use**")
    st.markdown(
        "1. Upload an MRI scan (JPG/PNG)\n"
        "2. Click **Predict**\n"
        "3. Review the result & confidence score"
    )
    st.markdown("---")
    st.caption("⚠️ For research/educational use only. Not a substitute for professional medical diagnosis.")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="monco-header">
        <p class="monco-title">MONCO</p>
        <p class="monco-subtitle">🧠 AI-Powered Brain Tumor Detection</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------------------------------------------------------------------------
# Upload card
# ---------------------------------------------------------------------------
st.markdown('<div class="monco-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload MRI Scan",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    # Center a smaller preview instead of full-width
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Uploaded MRI", width=280)

    predict_clicked = st.button("🔍 Predict")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------
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

    st.markdown('<div class="monco-card">', unsafe_allow_html=True)

    if response is not None and response.status_code == 200:
        data = response.json()
        prediction = data.get("prediction", "Unknown")
        confidence = data.get("confidence", 0)

        is_tumor = "no" not in str(prediction).lower() and "clear" not in str(prediction).lower() and "normal" not in str(prediction).lower()
        box_class = "result-tumor" if is_tumor else "result-clear"
        icon = "⚠️" if is_tumor else "✅"

        st.markdown(
            f'<div class="result-box {box_class}">{icon} Prediction: {prediction}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<p class="confidence-label">Confidence: {confidence}%</p>',
            unsafe_allow_html=True
        )
        st.progress(min(int(confidence), 100) / 100)

    else:
        st.error("❌ Prediction failed. Please check that the API server is running.")

    st.markdown('</div>', unsafe_allow_html=True)