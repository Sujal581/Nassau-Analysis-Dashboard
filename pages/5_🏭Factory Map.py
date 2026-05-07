import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE ----------------
st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Wholesale Candy",
    layout="wide",
    initial_sidebar_state="collapsed"   
)

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🏭 Factory Intelligence")

# ---------------- DATA ----------------
factory_data = pd.DataFrame({
    "Factory": [
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Sugar Shack",
        "Secret Factory",
        "The Other Factory"
    ],
    "lat": [
        32.881893,
        32.076176,
        48.11914,
        41.446333,
        35.1175
    ],
    "lon": [
        -111.768036,
        -81.088371,
        -96.18115,
        -90.565487,
        -89.971107
    ],
    "Region": [
        "West",
        "East",
        "North",
        "Midwest",
        "Midwest"
    ],
    "Capacity (Units)": [1200, 900, 1500, 800, 1100],
    "Status": ["Active", "Active", "Idle", "Active", "Maintenance"],

    # 🔥 SIMULATED PERFORMANCE METRICS (IMPORTANT)
    "Avg Lead Time": [12, 28, 6, 35, 18],
    "Delay Rate": [0.10, 0.42, 0.05, 0.55, 0.22],
    "Shipments": [500, 300, 700, 200, 450]
})

# ---------------- BOTTLENECK SCORE ----------------
factory_data["Bottleneck Score"] = (
    factory_data["Avg Lead Time"] * 0.6 +
    factory_data["Delay Rate"] * 100 * 0.4
)

# ---------------- RISK CLASSIFICATION ----------------
factory_data["Risk"] = factory_data["Bottleneck Score"].apply(
    lambda x: "Critical 🔴" if x > 30
    else "Warning 🟠" if x > 18
    else "Healthy 🟢"
)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([2, 1])

# ---------------- MAP (RISK BASED COLOR) ----------------
with col1:
    st.subheader("🗺️ Factory Risk Map")

    fig = px.scatter_mapbox(
        factory_data,
        lat="lat",
        lon="lon",
        hover_name="Factory",
        hover_data=[
            "Region",
            "Capacity (Units)",
            "Avg Lead Time",
            "Delay Rate",
            "Risk"
        ],
        color="Risk",
        color_discrete_map={
            "Healthy 🟢": "green",
            "Warning 🟠": "orange",
            "Critical 🔴": "red"
        },
        zoom=3,
        height=650
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- DETAILS PANEL ----------------
with col2:
    st.subheader("📌 Factory Intelligence Panel")

    selected_factory = st.selectbox(
        "Select Factory",
        factory_data["Factory"]
    )

    info = factory_data[
        factory_data["Factory"] == selected_factory
    ].iloc[0]

    st.markdown("### 🏭 Factory Overview")

    st.write("**Factory:**", info["Factory"])
    st.write("**Region:**", info["Region"])
    st.write("**Capacity:**", info["Capacity (Units)"])
    st.write("**Status:**", info["Status"])

    st.markdown("### 📊 Performance Metrics")
    st.write("Avg Lead Time:", info["Avg Lead Time"], "days")
    st.write("Delay Rate:", round(info["Delay Rate"] * 100, 1), "%")
    st.write("Bottleneck Score:", round(info["Bottleneck Score"], 2))

    # ---------------- STATUS ----------------
    if info["Risk"] == "Healthy 🟢":
        st.success("🟢 Factory is Operating Efficiently")
    elif info["Risk"] == "Warning 🟠":
        st.warning("🟠 Performance Degradation Detected")
    else:
        st.error("🔴 Critical Bottleneck Detected")

# ---------------- BOTTLENECK TABLE ----------------
st.markdown("### 🚧 Bottleneck Ranking")

ranked = factory_data.sort_values("Bottleneck Score", ascending=False)

st.dataframe(
    ranked[[
        "Factory",
        "Bottleneck Score",
        "Avg Lead Time",
        "Delay Rate",
        "Risk"
    ]],
    use_container_width=True
)