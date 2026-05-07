import streamlit as st
import plotly.express as px
from data_manager import apply_filters, load_initial_data,init_data
from utils import geo_analysis, load_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Wholesale Candy",
    layout="wide",
    initial_sidebar_state="collapsed"   
)

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🗺️ Geographic Analysis")

# ---------------- DATA ----------------
df= init_data()
df = apply_filters()
geo_df = geo_analysis(df)

# ---------------- BOTTLENECK DETECTION ----------------
threshold = geo_df["Avg_Lead_Time"].mean()

geo_df["Performance"] = geo_df["Avg_Lead_Time"].apply(
    lambda x: "Critical 🔴" if x > threshold * 1.3
    else "Slow 🟠" if x > threshold
    else "Good 🟢"
)

# ---------------- MAP (COLOR BY PERFORMANCE) ----------------
fig = px.choropleth(
    geo_df,
    locations='State/Province',
    locationmode='USA-states',
    color='Performance',
    scope="usa",
    color_discrete_map={
        "Good 🟢": "#8989EA",
        "Slow 🟠": "#ABA5B3",
        "Critical 🔴": "#FF0000"
    }
)

fig.update_layout(
    mapbox_style="carto-darkmatter",
    margin=dict(l=0, r=0, t=0, b=0)
)

fig.update_geos(
    showcoastlines=False,
    showframe=False,
    bgcolor="#e6e7e9",
    subunitcolor="#374151",
    countrycolor="#374151"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- BOTTLENECK TABLE ----------------
st.subheader("🚧 Bottleneck States (Top Problem Areas)")

bottlenecks = geo_df.sort_values(
    by="Avg_Lead_Time",
    ascending=False
).head(10)

st.dataframe(
    bottlenecks[["State/Province", "Avg_Lead_Time", "Performance"]],
    use_container_width=True
)

# ---------------- INSIGHT SUMMARY ----------------
st.markdown("### 🧠 Key Insight")

worst_state = bottlenecks.iloc[0]

st.warning(
    f"""
    ⚠️ **Highest bottleneck detected: {worst_state['State/Province']}**

    - Avg Lead Time: {worst_state['Avg_Lead_Time']} days  
    - Status: {worst_state['Performance']}

    👉 This state should be prioritized for logistics optimization.
    """
)