import pandas as pd

import streamlit as st

from services.api_client import (

    get_states,

    get_analysis_report,

    get_forecast
)

from components.sidebar import (
    render_sidebar
)

from components.charts import (

    render_historical_chart,

    render_trend_chart
)

render_sidebar()

st.title(
    "📊 State Climate Overview"
)

# -----------------------------------
# STATE SELECTION
# -----------------------------------

states = get_states()

available_states = [

    s["state"]

    for s in states

    if s["analysed"]
]

selected_state = st.selectbox(

    "Select State",

    available_states
)

# -----------------------------------
# LOAD REPORT
# -----------------------------------

report = get_analysis_report(
    selected_state
)

# -----------------------------------
# KPI CARDS
# -----------------------------------

st.subheader(
    "🌡️ Climate KPIs"
)

temperature_trend = (

    report["trend_analysis"]

    ["temperature"]

    ["trend_per_decade"]
)

rainfall_trend = (

    report["trend_analysis"]

    ["rainfall"]

    ["trend_per_decade"]
)

heatwaves = (

    report["extreme_events"]

    ["heatwaves"]

    ["event_count"]
)

extreme_rainfall = (

    report["extreme_events"]

    ["extreme_rainfall"]

    ["event_count"]
)

col1, col2, col3, col4 = (
    st.columns(4)
)

col1.metric(

    "Warming / Decade",

    f"{temperature_trend:.2f} °C"
)

col2.metric(

    "Rainfall Trend",

    f"{rainfall_trend:.2f}"
)

col3.metric(
    "Heatwaves",
    heatwaves
)

col4.metric(
    "Extreme Rainfall",
    extreme_rainfall
)

st.markdown("---")

# -----------------------------------
# DECADAL ANALYSIS
# -----------------------------------

st.subheader(
    "📈 Decadal Climate Evolution"
)

decadal_df = pd.DataFrame(
    report["decadal_analysis"]
)

st.dataframe(decadal_df)

# -----------------------------------
# TREND ANALYSIS
# -----------------------------------

st.subheader(
    "🔥 Climate Change Trends"
)

render_trend_chart(

    decadal_df,

    "avg_temperature",

    "Temperature Evolution"
)

render_trend_chart(

    decadal_df,

    "rainfall",

    "Rainfall Evolution"
)

st.markdown("---")

# -----------------------------------
# EXTREME YEARS
# -----------------------------------

st.subheader(
    "⚠️ Extreme Climate Years"
)

st.json(
    report["extreme_years"]
)

st.markdown("---")

# -----------------------------------
# FORECAST PREVIEW
# -----------------------------------

st.subheader(
    "🔮 Forecast Preview"
)

forecast = get_forecast(

    selected_state,

    horizon=12
)

st.json(forecast)

st.markdown("---")

# -----------------------------------
# CLIMATE NARRATIVE
# -----------------------------------

st.subheader(
    "🧠 Climate Intelligence Summary"
)

warming_text = (
    "warming"
    if temperature_trend > 0
    else "cooling"
)

st.info(

    f"""
    {selected_state} shows a long-term
    {warming_text} trend of
    {temperature_trend:.2f} °C
    per decade.

    The state has experienced
    {heatwaves} detected heatwave
    events and
    {extreme_rainfall} extreme
    rainfall events.

    Climate variability and
    seasonal shifts indicate
    ongoing environmental change.
    """
)