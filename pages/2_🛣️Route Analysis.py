import streamlit as st
import plotly.express as px
from data_manager import apply_filters, init_data, load_initial_data
from utils import load_data, route_analysis

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Wholesale Candy",
    layout="wide",
    initial_sidebar_state="collapsed"   
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}
</style>
""", unsafe_allow_html=True)

st.title("📈 Route Analysis")

# ---------------- DATA ----------------
df= init_data()
df = apply_filters()
route_df = route_analysis(df)

# ---------------- RANKING ----------------
route_df = route_df.sort_values(by="Avg_Lead_Time").reset_index(drop=True)
route_df["Rank"] = route_df.index + 1

# ---------------- LAYOUT ----------------
left, right = st.columns(2, gap="large")


# ---------------- FASTEST ROUTES ----------------
with left:
    st.subheader("🚀 Top 10 Fastest Routes")

    fastest = route_df.head(10).copy()

    fig1 = px.bar(
        fastest,
        x="Avg_Lead_Time",
        y="Route",
        orientation="h",
        color="Avg_Lead_Time",
        text="Rank",
        labels={
            "Avg_Lead_Time": "Avg Lead Time (Days)",
            "Route": "Route"
        }
    )

    fig1.update_traces(textposition="outside")

    fig1.update_layout(
        height=450,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    fig1.update_yaxes(autorange="reversed")

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="fastest_routes_chart"
    )

# ---------------- SLOWEST ROUTES ----------------
with right:
    st.subheader("🐢 Top 10 Slowest Routes")

    slowest = route_df.sort_values(
        by="Avg_Lead_Time",
        ascending=False
    ).head(10).copy()

    slowest["Rank"] = range(1, len(slowest) + 1)

    fig2 = px.bar(
        slowest,
        x="Avg_Lead_Time",
        y="Route",
        orientation="h",
        color="Avg_Lead_Time",
        text="Rank",
        labels={
            "Avg_Lead_Time": "Avg Lead Time (Days)",
            "Route": "Route"
        }
    )

    fig2.update_traces(textposition="outside")

    fig2.update_layout(
        height=450,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    fig2.update_yaxes(autorange="reversed")

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="slowest_routes_chart"
    )

# ---------------- FULL RANK TABLE ----------------
st.markdown("### 🏆 Full Route Ranking")

st.dataframe(
    route_df[["Rank", "Route", "Avg_Lead_Time"]],
    use_container_width=True
)