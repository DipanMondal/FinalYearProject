import pandas as pd

import pydeck as pdk

import streamlit as st

from utils.constants import (
    STATE_COORDINATES
)


def get_state_color(state):

    if (
        state["trained"]
        and state["analysed"]
    ):

        return [128, 0, 128]

    elif state["analysed"]:

        return [0, 255, 0]

    elif state["trained"]:

        return [255, 215, 0]

    elif state["ingested"]:

        return [0, 191, 255]

    return [120, 120, 120]


def render_india_map(states):

    rows = []

    for state in states:

        state_name = state["state"]

        if (
            state_name
            not in STATE_COORDINATES
        ):

            continue

        coords = (
            STATE_COORDINATES[state_name]
        )

        rows.append({

            "state": state_name,

            "lat": coords["lat"],

            "lon": coords["lon"],

            "color":
                get_state_color(state)
        })

    df = pd.DataFrame(rows)

    layer = pdk.Layer(

        "ScatterplotLayer",

        data=df,

        get_position="[lon, lat]",

        get_fill_color="color",

        get_radius=50000,

        pickable=True
    )

    view_state = pdk.ViewState(

        latitude=22.5,

        longitude=78.9,

        zoom=4.2
    )

    deck = pdk.Deck(

        layers=[layer],

        initial_view_state=view_state,

        tooltip={
            "text": "{state}"
        }
    )

    st.pydeck_chart(deck)