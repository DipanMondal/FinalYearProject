import streamlit as st

from services.api_client import (

    get_states,

    get_analysis_report
)

from components.sidebar import (
    render_sidebar
)

from components.charts import (
    render_seasonal_signature_chart
)

from components.alert_box import (
    render_alert_box
)

from utils.page_layout import setup_page

setup_page(
    page_title="Seasonal Climate Explorer",
    page_icon="🌦️"
)

render_sidebar()

st.title(
    "🌦️ Seasonal Climate Explorer"
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

    seasonal_signature = (
        report["seasonal_signature"]
    )

    months = seasonal_signature["months"]

    temperature_data = (
        seasonal_signature["temperature"]
    )

    rainfall_data = (
        seasonal_signature["rainfall"]
    )

    temperature_climatology = (
        seasonal_signature[
            "temperature_climatology"
        ]
    )

    rainfall_climatology = (
        seasonal_signature[
            "rainfall_climatology"
        ]
    )

    # -----------------------------------
    # YEAR SELECTION
    # -----------------------------------

    available_years = sorted(
        temperature_data.keys()
    )

    default_years = (
        available_years[-5:]
        if len(available_years) >= 5
        else available_years
    )

    selected_years = st.multiselect(

        "Select Years",

        options=available_years,

        default=default_years
    )

    st.markdown("---")

    # -----------------------------------
    # TEMPERATURE SIGNATURE
    # -----------------------------------

    st.subheader(
        "🌡️ Temperature Seasonal Signature"
    )

    render_seasonal_signature_chart(

        seasonal_data=temperature_data,

        climatology=
            temperature_climatology,

        months=months,

        title=(
            "Multi-Year Temperature "
            "Seasonal Signature"
        ),

        y_label="Temperature (°C)",

        selected_years=selected_years
    )

    st.markdown("---")

    # -----------------------------------
    # RAINFALL SIGNATURE
    # -----------------------------------

    st.subheader(
        "🌧️ Rainfall Seasonal Signature"
    )

    render_seasonal_signature_chart(

        seasonal_data=rainfall_data,

        climatology=
            rainfall_climatology,

        months=months,

        title=(
            "Multi-Year Rainfall "
            "Seasonal Signature"
        ),

        y_label="Rainfall",

        selected_years=selected_years
    )

    st.markdown("---")

    # -----------------------------------
    # SCIENTIFIC INSIGHTS
    # -----------------------------------

    st.subheader(
        "🧠 Seasonal Climate Insights"
    )

    st.info(
        """
        These seasonal signature plots
        compare month-wise climate
        behavior across multiple years.

        The thick climatology line
        represents the long-term
        monthly average pattern.

        Deviations from climatology
        indicate:
        - warming/cooling shifts,
        - monsoon variability,
        - seasonal instability,
        - changing climate regimes.
        """
    )
    
else:
    st.markdown("---")
    render_alert_box(message = "No state has been analyzed yet!") 