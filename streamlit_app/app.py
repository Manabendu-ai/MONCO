"""MONCO - AI Brain Tumor Classification dashboard.

This file only orchestrates: it wires together the API client, chart
builder, and UI components. Logic for each concern lives in its own module
so future features (auth, PDF reports, Grad-CAM) can be added without
touching this file much.
"""

import streamlit as st
from PIL import Image

from api_client import (
    predict,
    get_history,
    delete_history_item,
    history_image_url,
    PredictionError,
)
from charts import probability_bar_chart
from config import HISTORY_PAGE_SIZE
from ui_components import (
    inject_custom_css,
    render_hero,
    render_sidebar,
    render_prediction_badge,
    render_history_item,
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

analyze_tab, history_tab = st.tabs(["Analyze", "History"])

with analyze_tab:
    uploaded_file = st.file_uploader("Upload MRI Scan", type=["jpg", "jpeg", "png"])

    result = None
    error_message = None
    analyze_clicked = False

    if uploaded_file:
        image = Image.open(uploaded_file)
        col_image, col_prediction = st.columns([0.8, 1.3], gap="large")

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

with history_tab:
    st.markdown(
        '<div class="section-heading">Previous Scans</div>', unsafe_allow_html=True
    )

    if "history_offset" not in st.session_state:
        st.session_state.history_offset = 0

    refresh_col, _ = st.columns([1, 4])
    with refresh_col:
        if st.button("Refresh"):
            st.session_state.history_offset = 0

    try:
        records = get_history(
            limit=HISTORY_PAGE_SIZE, offset=st.session_state.history_offset
        )
    except PredictionError as exc:
        records = None
        st.error(str(exc))

    if records is not None:
        if not records:
            st.caption("No past scans yet. Analyze an MRI to build up history.")
        else:
            def _delete(history_id: int):
                try:
                    delete_history_item(history_id)
                    st.rerun()
                except PredictionError as exc:
                    st.error(str(exc))

            cols = st.columns(2, gap="medium")
            for i, record in enumerate(records):
                with cols[i % 2]:
                    render_history_item(
                        record,
                        history_image_url(record["image_path"]),
                        on_delete=_delete,
                    )

            nav_prev, nav_next = st.columns(2)
            with nav_prev:
                if st.session_state.history_offset > 0:
                    if st.button("⬅ Newer"):
                        st.session_state.history_offset = max(
                            0, st.session_state.history_offset - HISTORY_PAGE_SIZE
                        )
                        st.rerun()
            with nav_next:
                if len(records) == HISTORY_PAGE_SIZE:
                    if st.button("Older ➡"):
                        st.session_state.history_offset += HISTORY_PAGE_SIZE
                        st.rerun()

render_footer()
