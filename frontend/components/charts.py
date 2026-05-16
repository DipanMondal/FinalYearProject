import pandas as pd

import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import streamlit as st


CHART_FONT_SIZE = 18
CHART_TITLE_SIZE = 26
CHART_AXIS_TITLE_SIZE = 20
CHART_LEGEND_SIZE = 17

# chart config
def apply_chart_style(fig, height=500):
    fig.update_layout(
        height=height,

        font=dict(
            size=CHART_FONT_SIZE
        ),

        title=dict(
            font=dict(
                size=CHART_TITLE_SIZE
            )
        ),

        xaxis=dict(
            title_font=dict(
                size=CHART_AXIS_TITLE_SIZE
            ),
            tickfont=dict(
                size=CHART_FONT_SIZE
            )
        ),

        yaxis=dict(
            title_font=dict(
                size=CHART_AXIS_TITLE_SIZE
            ),
            tickfont=dict(
                size=CHART_FONT_SIZE
            )
        ),

        legend=dict(
            font=dict(
                size=CHART_LEGEND_SIZE
            )
        )
    )

    return fig

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

        yaxis_title=y_label
    )
    
    fig = apply_chart_style(
        fig = fig,
        height = 450
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

    fig = apply_chart_style(
        fig = fig,
        height = 450
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
def render_yearly_decadal_trend_chart(
    yearly_df,
    decadal_df,
    yearly_x_column,
    yearly_y_column,
    decadal_x_column,
    decadal_y_column,
    title,
    y_label
):

    fig = go.Figure()

    # -----------------------------------
    # Yearly average temperature line
    # -----------------------------------

    if not yearly_df.empty:

        fig.add_trace(
            go.Scatter(
                x=yearly_df[yearly_x_column],
                y=yearly_df[yearly_y_column],
                mode="lines+markers",
                name="Yearly Average",
                line=dict(
                    width=2
                ),
                marker=dict(
                    size=6
                )
            )
        )

    # -----------------------------------
    # Decadal highlighted points
    # -----------------------------------

    fig.add_trace(
        go.Scatter(
            x=decadal_df[decadal_x_column],
            y=decadal_df[decadal_y_column],
            mode="markers",
            name="Decadal Average",
            marker=dict(
                size=15,
                symbol="diamond",
                line=dict(
                    width=2
                )
            )
        )
    )

    # -----------------------------------
    # Trend line based on decadal values
    # -----------------------------------

    trend_df = decadal_df[
        [
            decadal_x_column,
            decadal_y_column
        ]
    ].dropna()

    if len(trend_df) >= 2:

        x_values = trend_df[decadal_x_column].astype(float)
        y_values = trend_df[decadal_y_column].astype(float)

        slope, intercept = np.polyfit(
            x_values,
            y_values,
            1
        )

        if not yearly_df.empty:
            x_min = yearly_df[yearly_x_column].min()
            x_max = yearly_df[yearly_x_column].max()
        else:
            x_min = x_values.min()
            x_max = x_values.max()

        trend_x = np.linspace(
            x_min,
            x_max,
            100
        )

        trend_y = (
            slope * trend_x
            + intercept
        )

        fig.add_trace(
            go.Scatter(
                x=trend_x,
                y=trend_y,
                mode="lines",
                name="Trend Line",
                line=dict(
                    width=3,
                    dash="dash"
                )
            )
        )

    fig.update_layout(
        title=title,
        height=520,
        xaxis_title="Year",
        yaxis_title=y_label,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig = apply_chart_style(
        fig = fig,
        
        height = 520
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "responsive": True,
            "displayModeBar": False
        }
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

        hovermode="x unified"
    )
    
    fig = apply_chart_style(
        fig = fig,
        height = 600
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

    y_label,
    
    bar_color = None
):

    fig = px.bar(

        df,

        x=x_column,

        y=y_column,

        title=title
    )
    
    if bar_color:
        fig.update_traces(
            marker_color=bar_color,
            marker_line_color=bar_color,
            opacity=0.92
        )

    fig.update_layout(

        xaxis_title="Decade",

        yaxis_title=y_label
    )
    
    fig = apply_chart_style(
        fig = fig,
        height = 500
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

        xaxis_title="Date",

        yaxis_title=y_label
    )
    
    fig = apply_chart_style(
        fig = fig,
        height = 500
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )
    
    
def render_volatility_chart(
    volatility_data,
    
    bar_color_map=None
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
        
        color="Metric",

        color_discrete_map=bar_color_map,

        title="Climate Volatility"
    )

    fig = apply_chart_style(
        fig = fig,
        height = 500
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

        hovermode="x unified"
    )
    
    fig = apply_chart_style(
        fig = fig,
        height = 550
    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )