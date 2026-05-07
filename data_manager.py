import streamlit as st
import pandas as pd
from utils import *

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Nassau Candy | Shipping Dashboard",
    layout="wide"
)

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_initial_data():
    df = load_data("Nassau Candy Distributor.csv")
    df = clean_data(df)
    df = feature_engineering(df, save=True)
    df = df.dropna(how="all")
    return df


def init_data():
    if "df" not in st.session_state:
        st.session_state.df = load_initial_data()

    return st.session_state.df

# -------------------- FILTER FUNCTION --------------------
def apply_filters():

    df = st.session_state.get("df")

    if df is None:
        st.error("⚠️ Data not loaded. Please refresh Home page.")
        st.stop()

    st.sidebar.header("🔍 Global Filters")

    # ----------- INIT SESSION STATE -----------
    if "date_range" not in st.session_state:
        st.session_state.date_range = [
            df['Order Date'].min(),
            df['Order Date'].max()
        ]

    if "state" not in st.session_state:
        st.session_state.state = "All"

    if "mode" not in st.session_state:
        st.session_state.mode = "All"

    if "delay" not in st.session_state:
        st.session_state.delay = 5

    if "reset" not in st.session_state:
        st.session_state.reset = False

    # ----------- RESET HANDLER -----------
    if st.session_state.reset:
        st.session_state.date_range = [
            df['Order Date'].min(),
            df['Order Date'].max()
        ]
        st.session_state.state = "All"
        st.session_state.mode = "All"
        st.session_state.delay = 5

        st.session_state.reset = False

    # ----------- SIDEBAR UI -----------

    # 📅 Date
    st.sidebar.date_input(
        "📅 Start Date",
        key="start_date"
    )

    st.sidebar.date_input(
        "📅 End Date",
        key="end_date"
    )

    # 🌍 State
    st.sidebar.selectbox(
        "🌍 State",
        ["All"] + list(df['State/Province'].unique()),
        key="state"
    )

    # 🚚 Mode
    st.sidebar.selectbox(
        "🚚 Ship Mode",
        ["All"] + list(df['Ship Mode'].unique()),
        key="mode"
    )

    # ⏱ Delay
    st.sidebar.slider(
        "⏱ Delay Threshold",
        1, 15,
        key="delay"
    )

    # 🔄 Reset Button
    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.reset = True
        st.rerun()

    # ----------- APPLY FILTERS -----------
    filtered_df = df.copy()

    # Date filter
    if "start_date" not in st.session_state:
        st.session_state.start_date = df['Order Date'].min()

    if "end_date" not in st.session_state:
        st.session_state.end_date = df['Order Date'].max()

    # State filter
    if st.session_state.state != "All":
        filtered_df = filtered_df[
            filtered_df['State/Province'] == st.session_state.state
        ]

    # Ship Mode filter
    if st.session_state.mode != "All":
        filtered_df = filtered_df[
            filtered_df['Ship Mode'] == st.session_state.mode
        ]

    # Delay logic
    if "Lead Time" in filtered_df.columns:
        filtered_df['Delayed'] = filtered_df['Lead Time'] > st.session_state.delay

    return filtered_df