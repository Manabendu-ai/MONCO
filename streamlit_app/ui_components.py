"""Reusable UI building blocks for the MONCO dashboard.

Every function here only renders Streamlit elements - no API calls, no
chart math - so the visual layer can be restyled without touching logic.
"""

import streamlit as st

from config import get_class_meta


def inject_custom_css():
    st.markdown(
        """
        <style>
            .stApp { background: #0f172a; }

            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }
            header[data-testid="stHeader"] { background: transparent; }

            .block-container { padding-top: 2rem; max-width: 1100px; }

            .monco-title {
                font-size: 2.5rem;
                font-weight: 700;
                color: #f1f5f9;
                text-align: center;
                margin-bottom: 0.1rem;
                letter-spacing: 0.03em;
            }
            .monco-subtitle {
                text-align: center;
                color: #94a3b8;
                font-size: 1.05rem;
                margin-bottom: 0.4rem;
            }
            .monco-tagline {
                text-align: center;
                color: #64748b;
                font-size: 0.92rem;
                max-width: 560px;
                margin: 0 auto 1.6rem auto;
                line-height: 1.4;
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
            div.stButton > button p { font-size: 0.95rem; white-space: nowrap; }
            div.stButton > button:hover { background: #1d4ed8; color: white; }

            .prediction-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                border: 1px solid;
                border-radius: 999px;
                padding: 0.45rem 1.1rem;
                margin-bottom: 0.6rem;
            }
            .badge-emoji { font-size: 1.2rem; line-height: 1; }
            .badge-label { font-size: 1.15rem; font-weight: 700; }

            .confidence-value {
                font-size: 1.6rem;
                font-weight: 700;
                color: #f1f5f9;
                margin: 0.3rem 0 0.3rem;
            }
            .confidence-caption {
                color: #94a3b8;
                font-size: 0.85rem;
                margin-bottom: 0.4rem;
            }

            .section-heading {
                color: #cbd5e1;
                font-size: 1rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin: 1.6rem 0 0.6rem;
            }

            .monco-footer {
                text-align: center;
                color: #64748b;
                font-size: 0.85rem;
                margin-top: 2.2rem;
                padding-top: 1rem;
                border-top: 1px solid #1e293b;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown('<div class="monco-title">🧠 MONCO</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="monco-subtitle">AI Brain Tumor Classification</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="monco-tagline">Upload a brain MRI image and receive an '
        'AI-assisted classification with a natural language explanation.</div>',
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown("### About MONCO")
        st.write(
            "MONCO analyzes MRI brain scans, classifies potential tumor types, "
            "and generates a natural-language explanation of each result."
        )
        st.markdown("---")
        st.markdown("**How to use**")
        st.markdown(
            "1. Upload an MRI scan (JPG/PNG)\n"
            "2. Click **Analyze MRI**\n"
            "3. Review the prediction, confidence, chart, and explanation"
        )
        st.markdown("---")
        st.caption(
            "For research and educational use only. Not a substitute for "
            "professional medical diagnosis."
        )
        st.markdown("---")
        st.caption("Owner: Manabendu Karfa")


def render_prediction_badge(prediction: str, confidence: float):
    meta = get_class_meta(prediction)
    st.markdown(
        f"""
        <div class="prediction-badge" style="border-color:{meta['color']}55; background:{meta['color']}18;">
            <span class="badge-emoji">{meta['emoji']}</span>
            <span class="badge-label" style="color:{meta['color']}">{meta['label']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="confidence-value">{confidence:.2f}%</div>', unsafe_allow_html=True)
    st.markdown('<div class="confidence-caption">Model confidence</div>', unsafe_allow_html=True)
    st.progress(min(float(confidence), 100) / 100)


def render_disclaimer():
    st.warning(
        "⚠️ This prediction is generated using Artificial Intelligence and is "
        "intended for educational purposes only. It should not replace "
        "professional medical diagnosis. Consult a qualified neurologist or radiologist."
    )


def render_footer():
    st.markdown('<div class="monco-footer">Owner: Manabendu Karfa</div>', unsafe_allow_html=True)
