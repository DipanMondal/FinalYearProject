import pandas as pd

import streamlit as st

from services.api_client import (

    get_states,

    get_forecast,

    get_historical_data
)

from components.sidebar import (
    render_sidebar
)

from components.charts import (
    render_forecast_chart
)

from components.alert_box import (
    render_alert_box
)

from utils.page_layout import setup_page

setup_page(
    page_title="Climate Forecasting Center",
    page_icon="🔮"
)

from utils.styles import apply_global_styles

apply_global_styles()

render_sidebar()

st.title(
    "🔮 Climate Forecasting Center"
)

# -----------------------------------
# STATE SELECTION
# -----------------------------------

states = get_states()

available_states = [

    s["state"]

    for s in states

    if s["trained"]
]

if len(available_states)!=0:

    selected_state = st.selectbox(

        "Select State",

        available_states
    )

    # -----------------------------------
    # FORECAST HORIZON
    # -----------------------------------

    forecast_horizon = st.slider(

        "Forecast Horizon (Months)",

        min_value=1,

        max_value=60,

        value=12
    )

    # -----------------------------------
    # LOAD DATA
    # -----------------------------------

    historical_data = (
        get_historical_data(
            selected_state
        )
    )

    forecast_data = get_forecast(

        selected_state,

        forecast_horizon
    )

    historical_df = pd.DataFrame(
        historical_data
    )

    # -----------------------------------
    # CREATE HISTORICAL DATES
    # -----------------------------------

    historical_df["date"] = pd.to_datetime({

        "year": historical_df["year"],

        "month": historical_df["month"],

        "day": 1
    })

    # -----------------------------------
    # TEMPERATURE FORECAST
    # -----------------------------------

    temperature_forecast = pd.DataFrame(

        forecast_data["data"]
        ["avg_temperature"]
    )

    temperature_forecast["date"] = (
        pd.to_datetime({

            "year":
                temperature_forecast[
                    "year"
                ],

            "month":
                temperature_forecast[
                    "month"
                ],

            "day": 1
        })
    )

    # -----------------------------------
    # RAINFALL FORECAST
    # -----------------------------------

    rainfall_forecast = pd.DataFrame(

        forecast_data["data"]
        ["rainfall"]
    )

    rainfall_forecast["date"] = (
        pd.to_datetime({

            "year":
                rainfall_forecast[
                    "year"
                ],

            "month":
                rainfall_forecast[
                    "month"
                ],

            "day": 1
        })
    )

    # -----------------------------------
    # HUMIDITY FORECAST
    # -----------------------------------

    humidity_forecast = pd.DataFrame(

        forecast_data["data"]
        ["humidity"]
    )

    humidity_forecast["date"] = (
        pd.to_datetime({

            "year":
                humidity_forecast[
                    "year"
                ],

            "month":
                humidity_forecast[
                    "month"
                ],

            "day": 1
        })
    )

    # -----------------------------------
    # FORECAST SUMMARY
    # -----------------------------------

    st.subheader(
        "📊 Forecast Summary"
    )

    latest_temp = (
        temperature_forecast[
            "prediction"
        ].iloc[-1]
    )

    latest_rainfall = (
        rainfall_forecast[
            "prediction"
        ].iloc[-1]
    )

    latest_humidity = (
        humidity_forecast[
            "prediction"
        ].iloc[-1]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Projected Temperature",

        f"{latest_temp:.2f} °C"
    )

    col2.metric(

        "Projected Rainfall",

        f"{latest_rainfall:.2f}"
    )

    col3.metric(

        "Projected Humidity",

        f"{latest_humidity:.2f}"
    )

    st.markdown("---")

    # -----------------------------------
    # TEMPERATURE FORECAST
    # -----------------------------------

    st.subheader(
        "🌡️ Temperature Forecast"
    )

    render_forecast_chart(

        historical_df,

        temperature_forecast,

        "avg_temperature",

        "prediction",

        "Temperature Projection",

        "Temperature (°C)"
    )

    st.markdown("---")

    # -----------------------------------
    # RAINFALL FORECAST
    # -----------------------------------

    st.subheader(
        "🌧️ Rainfall Forecast"
    )

    render_forecast_chart(

        historical_df,

        rainfall_forecast,

        "rainfall",

        "prediction",

        "Rainfall Projection",

        "Rainfall"
    )

    st.markdown("---")

    # -----------------------------------
    # HUMIDITY FORECAST
    # -----------------------------------

    st.subheader(
        "💧 Humidity Forecast"
    )

    render_forecast_chart(

        historical_df,

        humidity_forecast,

        "humidity",

        "prediction",

        "Humidity Projection",

        "Humidity"
    )

    st.markdown("---")

    # -----------------------------------
    # CLIMATE OUTLOOK
    # -----------------------------------

    st.subheader(
        "🧠 Climate Outlook"
    )

    st.info(

        f"""
        Forecast projections for
        {selected_state} suggest:

        - Future temperature:
          {latest_temp:.2f} °C

        - Future rainfall:
          {latest_rainfall:.2f}

        - Future humidity:
          {latest_humidity:.2f}

        Recursive forecasting models
        indicate continuing climate
        evolution over the selected
        forecast horizon.
        """
    )
    
else:
    st.markdown("---")
    render_alert_box(message = "No trained model available right now!")