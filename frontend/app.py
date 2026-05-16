import streamlit as st

from utils.page_layout import setup_page


setup_page(
    page_title="Climate Intelligence Platform",
    page_icon="🌍"
)

from utils.styles import apply_global_styles

apply_global_styles()


st.title(
    "🌍 Climate Intelligence Platform"
)

st.markdown("""
### Global Warming & Climate Analytics for India

Analyze:
- Temperature trends
- Rainfall patterns
- Humidity evolution
- Climate risk
- Forecasting insights
""")