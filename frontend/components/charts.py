import pandas as pd

import plotly.express as px

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
    
    
