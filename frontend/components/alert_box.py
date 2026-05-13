import streamlit as st


def render_alert_box(message:str):
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        # Display the red alert box
        st.error(f"🚨 {message}")