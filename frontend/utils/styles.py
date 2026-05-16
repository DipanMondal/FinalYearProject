import streamlit as st


def apply_global_styles():
    st.markdown(
        """
        <style>
        /* Main readable text */
        .stMarkdown,
        .stMarkdown p,
        .stMarkdown li {
            font-size: 18px !important;
            line-height: 1.6 !important;
        }

        /* Page headings */
        h1 {
            font-size: 2.4rem !important;
            line-height: 1.2 !important;
        }

        h2 {
            font-size: 2rem !important;
            line-height: 1.25 !important;
        }

        h3 {
            font-size: 1.6rem !important;
            line-height: 1.3 !important;
        }

        /* Buttons */
        .stButton button {
            font-size: 16px !important;
            padding: 0.45rem 0.8rem !important;
        }

        /* Input widgets */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {
            font-size: 16px !important;
        }

        /* Selectbox / multiselect labels only */
        label {
            font-size: 16px !important;
            font-weight: 500 !important;
        }

        /* ===============================
           KPI / Metric Styling
           =============================== */

        /* Whole KPI block */
        [data-testid="stMetric"] {
            padding: 0.85rem 1rem !important;
        }

        /* KPI header / label */
        [data-testid="stMetricLabel"] {
            font-size: 20px !important;
            line-height: 1.35 !important;
        }

        [data-testid="stMetricLabel"] p {
            font-size: 20px !important;
            font-weight: 700 !important;
            line-height: 1.35 !important;
            white-space: normal !important;
            overflow-wrap: break-word !important;
        }

        /* KPI main value */
        [data-testid="stMetricValue"] {
            font-size: 34px !important;
            line-height: 1.2 !important;
        }

        [data-testid="stMetricValue"] div {
            font-size: 34px !important;
            font-weight: 400 !important;
        }

        /* KPI delta, if used */
        [data-testid="stMetricDelta"] {
            font-size: 16px !important;
        }

        [data-testid="stMetricDelta"] div {
            font-size: 16px !important;
        }

         /* ===============================
           Sidebar Text
           =============================== */

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stMarkdown p {
            font-size: 16px !important;
        }

        /* Sidebar page navigation item */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
            font-size: 16px !important;
            font-weight: 400 !important;
            line-height: 1.4 !important;
            padding-top: 0.25rem !important;
            padding-bottom: 0.25rem !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a span {
            font-size: 15px !important;
            font-weight: 300 !important;
        }

        /* For newer Streamlit versions */
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
            font-size: 16px !important;
            font-weight: 400 !important;
            padding-top: 0.25rem !important;
            padding-bottom: 0.25rem !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span {
            font-size: 15px !important;
            font-weight: 300 !important;
        }

        /* Active page item */
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
            font-size: 16px !important;
            font-weight: 400 !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] span {
            font-size: 16px !important;
            font-weight: 400 !important;
        }
        
        /* ===============================
           Summary / Footer Info Box Styling
           Applies to st.info(), st.warning(), st.error(), st.success()
           =============================== */
        [data-testid="stAlert"] {
            padding: 0.5rem 0.5rem !important;
            border-radius: 10px !important;
        }

        [data-testid="stAlert"] p {
            font-size: 20px !important;
            line-height: 1.25 !important;
            font-weight: 500 !important;
        }

        [data-testid="stAlert"] li {
            font-size: 20px !important;
            line-height: 1.25 !important;
            font-weight: 500 !important;
        }

        [data-testid="stAlert"] div {
            font-size: 20px !important;
            line-height: 1.25 !important;
        }

        /* Responsive KPI adjustment */
        @media screen and (max-width: 768px) {
            [data-testid="stMetricLabel"],
            [data-testid="stMetricLabel"] p {
                font-size: 17px !important;
            }

            [data-testid="stMetricValue"],
            [data-testid="stMetricValue"] div {
                font-size: 28px !important;
            }

            [data-testid="stMetric"] {
                padding: 0.6rem 0.7rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )