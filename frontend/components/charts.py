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
    df,
    x_column,
    value_column,
    title
):

    fig = px.scatter(

        df,

        x=x_column,

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
    
    
def render_decadal_bar_chart(

    df,

    x_column,

    y_column,

    title,

    y_label
):

    fig = px.bar(

        df,

        x=x_column,

        y=y_column,

        title=title
    )

    fig.update_layout(

        height=500,

        xaxis_title="Decade",

        yaxis_title=y_label
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
    
def render_event_timeline(

    events,

    value_key,

    title,

    y_label
):

    if not events:

        st.warning(
            "No events detected."
        )

        return

    df = pd.DataFrame(events)

    df["date"] = pd.to_datetime({

        "year": df["year"],

        "month": df["month"],

        "day": 1
    })

    fig = px.scatter(

        df,

        x="date",

        y=value_key,

        size=value_key,

        title=title
    )

    fig.update_layout(

        height=500,

        xaxis_title="Date",

        yaxis_title=y_label
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
    
def render_volatility_chart(
    volatility_data
):

    df = pd.DataFrame({

        "Metric": [

            "Temperature",

            "Rainfall",

            "Humidity"
        ],

        "Volatility": [

            volatility_data[
                "temperature_volatility"
            ],

            volatility_data[
                "rainfall_volatility"
            ],

            volatility_data[
                "humidity_volatility"
            ]
        ]
    })

    fig = px.bar(

        df,

        x="Metric",

        y="Volatility",

        title="Climate Volatility"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
    
    
def render_forecast_chart(

    historical_df,

    forecast_df,

    value_column,

    forecast_column,

    title,

    y_label
):

    fig = go.Figure()

    # -----------------------------------
    # Historical
    # -----------------------------------

    fig.add_trace(

        go.Scatter(

            x=historical_df["date"],

            y=historical_df[value_column],

            mode="lines",

            name="Historical"
        )
    )

    # -----------------------------------
    # Forecast
    # -----------------------------------

    fig.add_trace(

        go.Scatter(

            x=forecast_df["date"],

            y=forecast_df[forecast_column],

            mode="lines",

            name="Forecast"
        )
    )

    fig.update_layout(

        title=title,

        xaxis_title="Date",

        yaxis_title=y_label,

        height=550,

        hovermode="x unified"
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
