import pandas as pd

import streamlit as st

from services.api_client import (

    get_states,

    get_analysis_report
)

from components.sidebar import (
    render_sidebar
)

from components.charts import (

    render_trend_chart,

    render_decadal_bar_chart,
    
    render_yearly_decadal_trend_chart
)

from components.alert_box import (
    render_alert_box
)

from utils.report_transformers import build_yearly_average_df

from utils.page_layout import setup_page

setup_page(
    page_title="Climate Change Trends",
    page_icon="📈"
)

from utils.styles import apply_global_styles

from utils.chart_colors import CLIMATE_BAR_COLORS

apply_global_styles()

render_sidebar()

st.title(
    "📈 Climate Change Trends"
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

if len(available_states)!=0:

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

    trend_analysis = (
        report["trend_analysis"]
    )

    decadal_analysis = (
        report["decadal_analysis"]
    )

    decadal_df = pd.DataFrame(
        decadal_analysis
    )
    
    yearly_temperature_df = build_yearly_average_df(
        report,
        metric_key="temperature",
        output_column="avg_temperature"
    )
    
    yearly_rainfall_df = build_yearly_average_df(
        report,
        metric_key="rainfall",
        output_column="rainfall"
    )

    # -----------------------------------
    # KPI SECTION
    # -----------------------------------

    st.subheader(
        "🌍 Climate Change Indicators"
    )

    temp_trend = (
        trend_analysis["temperature"]
    )

    rainfall_trend = (
        trend_analysis["rainfall"]
    )

    humidity_trend = (
        trend_analysis["humidity"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Warming Rate",

        (
            f"{temp_trend['trend_per_decade']:.2f}"
            " °C / decade"
        )
    )

    col2.metric(

        "Rainfall Trend",

        (
            f"{rainfall_trend['trend_per_decade']:.2f}"
        )
    )

    col3.metric(

        "Humidity Trend",

        (
            f"{humidity_trend['trend_per_decade']:.2f}"
        )
    )

    st.markdown("---")

    # -----------------------------------
    # STATISTICAL METRICS
    # -----------------------------------

    st.subheader(
        "📊 Statistical Significance"
    )

    stats_df = pd.DataFrame({

        "Metric": [

            "Temperature R²",
            "Rainfall R²",
            "Humidity R²",

            "Temperature p-value",
            "Rainfall p-value",
            "Humidity p-value"
        ],

        "Value": [

            temp_trend["r_squared"],
            rainfall_trend["r_squared"],
            humidity_trend["r_squared"],

            temp_trend["p_value"],
            rainfall_trend["p_value"],
            humidity_trend["p_value"]
        ]
    })

    st.dataframe(stats_df)

    st.markdown("---")

    # -----------------------------------
    # TEMPERATURE EVOLUTION
    # -----------------------------------

    st.subheader(
        "🔥 Temperature Evolution"
    )

    render_yearly_decadal_trend_chart(

        yearly_df=yearly_temperature_df,

        decadal_df=decadal_df,

        yearly_x_column="year",

        yearly_y_column="avg_temperature",

        decadal_x_column="decade",

        decadal_y_column="avg_temperature",

        title=f"{selected_state} Yearly Temperature Evolution with Decadal Highlights",

        y_label="Temperature (°C)"
    )

    render_decadal_bar_chart(

        decadal_df,

        "decade",

        "avg_temperature",

        f"{selected_state} Average Temperature by Decade",

        "Temperature (°C)",
        
        bar_color=CLIMATE_BAR_COLORS["temperature"]
    )

    st.markdown("---")

    # -----------------------------------
    # RAINFALL EVOLUTION
    # -----------------------------------

    st.subheader(
        "🌧️ Rainfall Evolution"
    )

    render_yearly_decadal_trend_chart(

        yearly_df=yearly_rainfall_df,

        decadal_df=decadal_df,

        yearly_x_column="year",

        yearly_y_column="rainfall",

        decadal_x_column="decade",

        decadal_y_column="rainfall",

        title=f"{selected_state} Rainfall Evolution",

        y_label="Rainfall"
    )

    render_decadal_bar_chart(

        decadal_df,

        "decade",

        "rainfall",

        f"{selected_state} Average Rainfall by Decade",

        "Rainfall",
        
        bar_color=CLIMATE_BAR_COLORS["rainfall"]
    )

    st.markdown("---")

    # -----------------------------------
    # HUMIDITY EVOLUTION
    # -----------------------------------

    st.subheader(
        "💧 Humidity Evolution"
    )

    render_trend_chart(

        decadal_df,

        "decade",

        "humidity",

        f"{selected_state} Decadal Humidity Change"
    )

    render_decadal_bar_chart(

        decadal_df,

        "decade",

        "humidity",

        f"{selected_state} Average Humidity by Decade",

        "Humidity",
        
        bar_color=CLIMATE_BAR_COLORS["humidity"]
    )

    st.markdown("---")

    # -----------------------------------
    # SCIENTIFIC INTERPRETATION
    # -----------------------------------

    st.subheader(
        "🧠 Climate Interpretation"
    )

    warming_direction = (

        "warming"

        if temp_trend[
            "trend_per_decade"
        ] > 0

        else "cooling"
    )

    significance = (

        "statistically significant"

        if temp_trend["p_value"] < 0.05

        else "weakly significant"
    )

    st.info(

        f"""
        {selected_state} demonstrates a
        long-term {warming_direction}
        climate trend.

        The estimated temperature
        change is
        {temp_trend['trend_per_decade']:.2f}
        °C per decade.

        The observed trend appears
        {significance}
        with an R² value of
        {temp_trend['r_squared']:.3f}.

        Rainfall and humidity trends
        indicate evolving seasonal
        climate dynamics over time.
        """
    )
    
else:
    st.markdown("---")
    render_alert_box(message = "No state is analysed yet!")
