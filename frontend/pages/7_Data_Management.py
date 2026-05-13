import streamlit as st

from services.api_client import (

    get_states,

    generate_features,

    train_state,

    run_analysis,

    delete_state_data,

    delete_models,

    delete_analysis
)

from components.sidebar import (
    render_sidebar
)

from components.alert_box import (
    render_alert_box
)


render_sidebar()

st.title(
    "🛠️ Data & Model Management"
)

# -----------------------------------
# LOAD STATES
# -----------------------------------

states = get_states()

st.subheader(
    "📋 State Lifecycle Status"
)

st.dataframe(states)

st.markdown("---")

# -----------------------------------
# STATE SELECTION
# -----------------------------------

available_states = [

    s["state"]
    for s in states
]

if len(available_states)!=0:

    selected_state = st.selectbox(

        "Select State",

        available_states
    )

    st.markdown("---")

    # -----------------------------------
    # PIPELINE ACTIONS
    # -----------------------------------

    st.subheader(
        "⚙️ Pipeline Operations"
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    # -----------------------------------
    # FEATURE GENERATION
    # -----------------------------------

    if col1.button(
        "Regenerate Features"
    ):

        response = generate_features(
            selected_state
        )

        st.success(response)

    # -----------------------------------
    # RETRAIN MODELS
    # -----------------------------------

    if col2.button(
        "Retrain Models"
    ):

        response = train_state(
            selected_state
        )

        st.success(response)

    # -----------------------------------
    # REGENERATE ANALYSIS
    # -----------------------------------

    if col3.button(
        "Regenerate Analysis"
    ):

        response = run_analysis(
            selected_state
        )

        st.success(response)

    st.markdown("---")

    # -----------------------------------
    # DESTRUCTIVE ACTIONS
    # -----------------------------------

    st.subheader(
        "⚠️ Destructive Operations"
    )

    danger1, danger2, danger3 = (
        st.columns(3)
    )

    # -----------------------------------
    # DELETE DATA
    # -----------------------------------

    if danger1.button(
        "Delete State Data"
    ):

        response = delete_state_data(
            selected_state
        )

        st.error(response)

    # -----------------------------------
    # DELETE MODELS
    # -----------------------------------

    if danger2.button(
        "Delete Models"
    ):

        response = delete_models(
            selected_state
        )

        st.error(response)

    # -----------------------------------
    # DELETE ANALYSIS
    # -----------------------------------

    if danger3.button(
        "Delete Analysis"
    ):

        response = delete_analysis(
            selected_state
        )

        st.error(response)

    st.markdown("---")

    # -----------------------------------
    # SYSTEM HEALTH
    # -----------------------------------

    st.subheader(
        "🖥️ System Health"
    )

    total_states = len(states)

    trained_states = sum(

        1 for s in states

        if s["trained"]
    )

    analysed_states = sum(

        1 for s in states

        if s["analysed"]
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    col1.metric(
        "States",
        total_states
    )

    col2.metric(
        "Models Ready",
        trained_states
    )

    col3.metric(
        "Analysis Ready",
        analysed_states
    )

    st.markdown("---")

    # -----------------------------------
    # PLATFORM INFO
    # -----------------------------------

    st.subheader(
        "ℹ️ Platform Information"
    )

    st.info(
        """
        Climate Intelligence Platform

        Features:
        - Climate ingestion
        - Feature engineering
        - Recursive forecasting
        - SARIMAX modeling
        - Trend analysis
        - Extreme-event analytics
        - Climate risk assessment
        """
    )
    
else:
    st.markdown("---")
    render_alert_box(message = "No state is registered. Please register a state from Home menu in the sidebar")