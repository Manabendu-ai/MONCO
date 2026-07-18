"""MONCO - AI Brain Tumor Classification dashboard.

This file only orchestrates: it wires together the API client, chart
builder, and UI components. Logic for each concern lives in its own module
so future features (auth, history, PDF reports, Grad-CAM) can be added
without touching this file much.
"""

import streamlit as st
from PIL import Image

from api_client import predict, PredictionError
from charts import probability_bar_chart
from ui_components import (
    inject_custom_css,
    render_hero,
    render_sidebar,
    render_prediction_badge,
    render_disclaimer,
    render_footer,
)

st.set_page_config(
    page_title="MONCO",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
render_sidebar()
render_hero()

uploaded_file = st.file_uploader("Upload MRI Scan", type=["jpg", "jpeg", "png"])

result = None
error_message = None
analyze_clicked = False

if uploaded_file:
    image = Image.open(uploaded_file)
    col_image, col_prediction = st.columns([1, 1.3], gap="large")

    with col_image:
        with st.container(border=True):
            st.image(image, caption="Uploaded MRI", use_container_width=True)
            analyze_clicked = st.button("Analyze MRI")

    with col_prediction:
        with st.container(border=True):
            if analyze_clicked:
                with st.status("Running Deep Learning Model...", expanded=False) as status:
                    try:
                        result = predict(
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                        status.update(label="Generating AI Explanation...", state="running")
                        status.update(label="Analysis complete", state="complete")
                    except PredictionError as exc:
                        error_message = str(exc)
                        status.update(label="Analysis failed", state="error")

                if error_message:
                    st.error(error_message)
                elif result:
                    render_prediction_badge(result["prediction"], result["confidence"])
            else:
                st.caption("Upload an MRI and click Analyze MRI to see results here.")

    if result:
        st.markdown('<div class="section-heading">Probability Distribution</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.plotly_chart(
                probability_bar_chart(result["probabilities"]),
                use_container_width=True,
            )

        st.markdown('<div class="section-heading">AI Explanation</div>', unsafe_allow_html=True)
        with st.expander("AI Explanation", expanded=True):
            st.markdown(result.get("explanation", "No explanation available."))

st.write("")
render_disclaimer()
render_footer()
