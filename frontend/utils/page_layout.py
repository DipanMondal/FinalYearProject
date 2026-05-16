import streamlit as st


def setup_page(
    page_title: str,
    page_icon: str = "🌍",
    sidebar_state: str = "expanded"
):
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state=sidebar_state
    )

    apply_responsive_layout()


def apply_responsive_layout():
    st.markdown(
        """
        <style>
        /* Make the main content use the full available page width */
        [data-testid="stAppViewContainer"] .main .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding-left: clamp(1rem, 2vw, 2.5rem) !important;
            padding-right: clamp(1rem, 2vw, 2.5rem) !important;
            padding-top: 2rem !important;
        }

        /* Fallback for different Streamlit versions */
        .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding-left: clamp(1rem, 2vw, 2.5rem) !important;
            padding-right: clamp(1rem, 2vw, 2.5rem) !important;
        }

        /* Make Plotly charts expand properly */
        [data-testid="stPlotlyChart"] {
            width: 100% !important;
        }

        [data-testid="stPlotlyChart"] > div {
            width: 100% !important;
        }

        /* Make dataframes use available width */
        [data-testid="stDataFrame"] {
            width: 100% !important;
        }

        /* Better spacing between responsive columns */
        [data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }

        /* Mobile/tablet responsiveness */
        @media screen and (max-width: 768px) {
            [data-testid="stAppViewContainer"] .main .block-container,
            .block-container {
                padding-left: 0.8rem !important;
                padding-right: 0.8rem !important;
                padding-top: 1rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )