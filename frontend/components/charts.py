import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import streamlit as st


def render_historical_chart(
    df,
    value_column,
    title,
    y_label
):

    fig = px.line(

        df,

        x="date",

        y=value_column,

        title=title
    )

    fig.update_layout(

        xaxis_title="Date",

        yaxis_title=y_label,

        height=450
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
    
def render_trend_chart(
    yearly_df,
    value_column,
    title
):

    fig = px.scatter(

        yearly_df,

        x=yearly_df.columns[0],

        y=value_column,

        trendline="ols",

        title=title
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
    
def render_seasonal_signature_chart(

    seasonal_data,

    climatology,

    months,

    title,

    y_label,

    selected_years
):

    fig = go.Figure()

    # -----------------------------------
    # Yearly Lines
    # -----------------------------------

    for year in selected_years:

        if year not in seasonal_data:

            continue

        fig.add_trace(

            go.Scatter(

                x=months,

                y=seasonal_data[year],

                mode="lines",

                name=year,

                opacity=0.6
            )
        )

    # -----------------------------------
    # Climatology Baseline
    # -----------------------------------

    fig.add_trace(

        go.Scatter(

            x=months,

            y=climatology,

            mode="lines",

            name="Climatology",

            line=dict(width=5)
        )
    )

    fig.update_layout(

        title=title,

        xaxis_title="Month",

        yaxis_title=y_label,

        height=600,

        hovermode="x unified"
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
