import streamlit as st

from services.api_client import (

    get_states,

    get_analysis_report
)

from components.sidebar import (
    render_sidebar
)

from components.charts import (

    render_event_timeline,

    render_volatility_chart
)

render_sidebar()

st.title(
    "⚠️ Extreme Events & Climate Risk"
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

extreme_events = (
    report["extreme_events"]
)

volatility_analysis = (
    report["volatility_analysis"]
)

anomaly_frequency = (
    report["anomaly_frequency"]
)

# -----------------------------------
# KPI SECTION
# -----------------------------------

st.subheader(
    "🚨 Climate Risk Indicators"
)

heatwave_count = (

    extreme_events["heatwaves"]

    ["event_count"]
)

rainfall_count = (

    extreme_events[
        "extreme_rainfall"
    ]

    ["event_count"]
)

humidity_count = (

    extreme_events[
        "high_humidity"
    ]

    ["event_count"]
)

risk_score = (
    heatwave_count
    + rainfall_count
    + humidity_count
)

col1, col2, col3, col4 = (
    st.columns(4)
)

col1.metric(
    "Heatwaves",
    heatwave_count
)

col2.metric(
    "Extreme Rainfall",
    rainfall_count
)

col3.metric(
    "Humidity Extremes",
    humidity_count
)

col4.metric(
    "Climate Risk Score",
    risk_score
)

st.markdown("---")

# -----------------------------------
# HEATWAVE TIMELINE
# -----------------------------------

st.subheader(
    "🔥 Heatwave Timeline"
)

render_event_timeline(

    extreme_events[
        "heatwaves"
    ]["events"],

    "temperature",

    "Heatwave Events",

    "Temperature (°C)"
)

st.markdown("---")

# -----------------------------------
# EXTREME RAINFALL TIMELINE
# -----------------------------------

st.subheader(
    "🌧️ Extreme Rainfall Timeline"
)

render_event_timeline(

    extreme_events[
        "extreme_rainfall"
    ]["events"],

    "rainfall",

    "Extreme Rainfall Events",

    "Rainfall"
)

st.markdown("---")

# -----------------------------------
# HUMIDITY EVENTS
# -----------------------------------

st.subheader(
    "💧 High Humidity Events"
)

render_event_timeline(

    extreme_events[
        "high_humidity"
    ]["events"],

    "humidity",

    "High Humidity Events",

    "Humidity"
)

st.markdown("---")

# -----------------------------------
# VOLATILITY ANALYSIS
# -----------------------------------

st.subheader(
    "📊 Climate Volatility"
)

render_volatility_chart(
    volatility_analysis
)

st.markdown("---")

# -----------------------------------
# ANOMALY FREQUENCY
# -----------------------------------

st.subheader(
    "📈 Anomaly Frequency"
)

st.json(anomaly_frequency)

st.markdown("---")

# -----------------------------------
# RISK INTERPRETATION
# -----------------------------------

st.subheader(
    "🧠 Climate Risk Interpretation"
)

risk_level = (

    "HIGH"

    if risk_score > 50

    else "MODERATE"

    if risk_score > 20

    else "LOW"
)

st.error(

    f"""
    Climate Risk Level:
    {risk_level}

    {selected_state} has experienced
    {heatwave_count} heatwave events,
    {rainfall_count} extreme rainfall
    events, and
    {humidity_count} high humidity
    anomalies.

    Elevated climate volatility and
    anomaly frequency suggest
    increasing environmental
    instability.
    """
)