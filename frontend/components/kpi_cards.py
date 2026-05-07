import streamlit as st


def render_kpi_cards(states):

    total_states = len(states)

    ingested = sum(
        1 for s in states
        if s["ingested"]
    )

    trained = sum(
        1 for s in states
        if s["trained"]
    )

    analysed = sum(
        1 for s in states
        if s["analysed"]
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        "States",
        total_states
    )

    col2.metric(
        "Ingested",
        ingested
    )

    col3.metric(
        "Models Trained",
        trained
    )

    col4.metric(
        "Analysis Ready",
        analysed
    )