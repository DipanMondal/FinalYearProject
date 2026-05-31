import streamlit as st

from services.api_client import (
    get_states,
    get_ai_insight_report,
    run_analysis
)

from components.sidebar import (
    render_sidebar
)

from components.alert_box import (
    render_alert_box
)

from utils.page_layout import setup_page


setup_page(
    page_title="AI Climate Insight",
    page_icon="🤖"
)

from utils.styles import apply_global_styles

apply_global_styles()

render_sidebar()

st.title(
    "🤖 AI Climate Insight"
)

st.caption(
    "Gemini-powered climate interpretation generated as part of the existing analysis pipeline."
)

states = get_states()

available_states = [

    s["state"]

    for s in states

    if s["analysed"]
]

if len(available_states) != 0:

    selected_state = st.selectbox(

        "Select State",

        available_states
    )

    col1, col2 = st.columns([1, 2])

    if col1.button("Regenerate Analysis + AI Insight"):

        with st.spinner("Running statistical analysis and AI insight generation..."):

            response = run_analysis(selected_state)

            st.success(response)

    st.markdown("---")

    insight = get_ai_insight_report(
        selected_state
    )

    if not insight.get("success", False):

        st.error(
            insight.get(
                "error",
                "AI insight report is not available. Regenerate analysis first."
            )
        )

        st.info(
            "Go to Data & Model Management and click Regenerate Analysis after adding GOOGLE_API_KEY in backend .env."
        )

    else:

        st.subheader(
            "📌 Report Metadata"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Rows Used",
            insight.get("rows_used", "N/A")
        )

        c2.metric(
            "Model",
            insight.get("model", "N/A")
        )

        c3.metric(
            "Forecast Horizon",
            f"{insight.get('forecast_horizon', 12)} months"
        )

        year_range = insight.get("year_range", {})

        st.caption(
            f"Generated at: {insight.get('generated_at', 'N/A')} | "
            f"Data range: {year_range.get('start_year', 'N/A')} - {year_range.get('end_year', 'N/A')}"
        )

        st.markdown("---")

        st.subheader(
            "🧠 AI-Generated Climate Analysis"
        )

        st.markdown(
            insight.get("report_markdown", "No AI report text found.")
        )

else:

    st.markdown("---")

    render_alert_box(
        message="No analysed state available. Run analysis first."
    )