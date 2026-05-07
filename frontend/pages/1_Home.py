import streamlit as st

from services.api_client import (
    get_states,

    ingest_state,

    generate_features,

    train_state,

    run_analysis
)

from components.sidebar import (
    render_sidebar
)

from components.kpi_cards import (
    render_kpi_cards
)

from components.india_map import (
    render_india_map
)


render_sidebar()

st.title(
    "🌍 Climate Intelligence Dashboard"
)

states = get_states()

# -----------------------------------
# KPI CARDS
# -----------------------------------

render_kpi_cards(states)

st.markdown("---")

# -----------------------------------
# INDIA MAP
# -----------------------------------

st.subheader(
    "🇮🇳 India Climate Pipeline Map"
)

render_india_map(states)

st.markdown("---")

# -----------------------------------
# STATE TABLE
# -----------------------------------

st.subheader(
    "📋 State Lifecycle Status"
)

st.dataframe(states)

st.markdown("---")

# -----------------------------------
# QUICK ACTIONS
# -----------------------------------

st.subheader(
    "⚙️ Quick Actions"
)

state_name = st.text_input(
    "State Name",
    "West Bengal"
)

col1, col2, col3, col4 = (
    st.columns(4)
)

# -----------------------------------
# INGEST
# -----------------------------------

if col1.button("Ingest Data"):

    response = ingest_state(

        state=state_name,

        start_year=2000,

        end_year=2020
    )

    st.success(response)

# -----------------------------------
# FEATURES
# -----------------------------------

if col2.button(
    "Generate Features"
):

    response = generate_features(
        state_name
    )

    st.success(response)

# -----------------------------------
# TRAIN
# -----------------------------------

if col3.button("Train Models"):

    response = train_state(
        state_name
    )

    st.success(response)

# -----------------------------------
# ANALYSIS
# -----------------------------------

if col4.button(
    "Generate Analysis"
):

    response = run_analysis(
        state_name
    )

    st.success(response)