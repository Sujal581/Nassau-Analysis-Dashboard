import streamlit as st
import plotly.express as px
import pandas as pd
from data_manager import apply_filters, init_data, load_initial_data
from utils import load_data, route_analysis, ship_mode_analysis

#---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_icon="🍪",
    page_title="Nassau Candy | Wholesale Candy",
    layout="wide",
    initial_sidebar_state="collapsed"   
)

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Optional hover effect */
div[data-testid="column"] > div:hover {
    transform: translateY(-3px);
    transition: 0.2s;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📊 Overview")
st.caption("Key performance indicators and summary of shipping operations")

# ALWAYS load safely
df = init_data()
df = apply_filters()

#---------------- KPI----------------
def kpi_card(title, value, icon="📊", color="#2563eb"):
    st.markdown(
        f"""
        <div style="
            background: {color}15;
            border-left: 5px solid {color};
            padding: 12px;
            border-radius: 10px;
            display: flex;
            gap: 10px;
            align-items: center;
        ">
            <div style="font-size:20px;">{icon}</div>
            <div>
                <div style="font-size:12px;color:gray;">{title}</div>
                <div style="font-size:18px;font-weight:bold;">{value}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- KPI CALCULATIONS ----------------
avg_lead = df['Lead Time'].mean()
total_orders = len(df)
delayed_orders = df['Delayed'].sum()
delay_pct = df['Delayed'].mean() * 100
efficiency = 1 / (avg_lead + 1)

# ---------------- FORMAT VALUES ----------------
avg_lead_f = f"{avg_lead:.1f} days"
total_orders_f = f"{total_orders:,}"
delayed_orders_f = f"{delayed_orders:,}"
delay_pct_f = f"{delay_pct:.1f}%"
efficiency_f = f"{efficiency:.3f}"

# ---------------- KPI GRID (RESPONSIVE) ----------------
cards = [
    ("Avg Lead Time", avg_lead_f, "⏱️", "#2563eb"),
    ("Total Shipments", total_orders_f, "📦", "#16a34a"),
    ("Delayed Shipments", delayed_orders_f, "🚚", "#f59e0b"),
    ("Delay Rate", delay_pct_f, "⚠️", "#dc2626"),
    ("Efficiency Score", efficiency_f, "🚀", "#9333ea"),
]

for i in range(0, len(cards), 3):
    cols = st.columns(3)
    for col, (title, value, icon, color) in zip(cols, cards[i:i+3]):
        with col:
            kpi_card(title, value, icon, color)

# ---------------- CHARTS ----------------
colA, colB = st.columns(2)

with colA:
    st.markdown("### 📈 Average Lead Time Over Time")

    trend = df.copy()
    trend['Month'] = trend['Order Date'].dt.to_period("M").dt.to_timestamp()
    trend_df = trend.groupby('Month')['Lead Time'].mean().reset_index()

    fig = px.line(trend_df, x='Month', y='Lead Time', markers=True)

    fig.update_layout(
        height=350,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

with colB:
    st.markdown("### 🚚 Shipments by Ship Mode")

    mode_df = ship_mode_analysis(df).sort_values(by="Shipments", ascending=False)

    fig2 = px.bar(mode_df, x='Ship Mode', y='Shipments', text='Shipments', color='Ship Mode')

    fig2.update_layout(
        height=350,
        template="plotly_dark",
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig2, use_container_width=True)

# ---------------- TABLES ----------------
colC, colD, colE = st.columns(3)
route_df = route_analysis(df)

# Fastest
# ---------------- TABLES ----------------
colC, colD, colE = st.columns(3)

route_df = route_analysis(df)

# ---------------- FASTEST ROUTES ----------------
with colC:
    st.markdown("#### 🚀 Fastest Routes")

    fastest = route_df.sort_values(by="Avg_Lead_Time").head(5).copy()
    fastest.columns = ["Route", "Avg Lead Time", "Shipments", "Delay %"]

    fastest["Avg Lead Time"] = fastest["Avg Lead Time"].round(1)
    

    fastest.insert(0, "Rank", range(1, len(fastest) + 1))

    # 🎨 Styling
    styled_fast = fastest.style \
        .background_gradient(subset=["Avg Lead Time"], cmap="Greens_r") \
        .background_gradient(subset=["Delay %"], cmap="Reds") \
        .format({
            "Avg Lead Time": "{:.1f}",
            "Delay %": "{:.1f}%"
        }) \
        .set_properties(**{"text-align": "center"}) \
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]}
        ])

    st.dataframe(styled_fast, use_container_width=True)


# ---------------- SLOWEST ROUTES ----------------
with colD:
    st.markdown("#### 🐢 Slowest Routes")

    slowest = route_df.sort_values(by="Avg_Lead_Time", ascending=False).head(5).copy()
    slowest.columns = ["Route", "Avg Lead Time", "Shipments", "Delay %"]

    slowest["Avg Lead Time"] = slowest["Avg Lead Time"].round(1)

    slowest.insert(0, "Rank", range(1, len(slowest) + 1))

    # 🎨 Styling
    styled_slow = slowest.style \
        .background_gradient(subset=["Avg Lead Time"], cmap="Reds") \
        .background_gradient(subset=["Delay %"], cmap="Reds") \
        .format({
            "Avg Lead Time": "{:.1f}",
            "Delay %": "{:.1f}%"
        }) \
        .set_properties(**{"text-align": "center"}) \
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]}
        ])

    st.dataframe(styled_slow, use_container_width=True)


# ---------------- TOP STATES ----------------
with colE:
    st.markdown("#### ⚠️ Top States by Delay Rate")

    state_df = df.groupby('State/Province').agg(
        Delay_Rate=('Delayed', 'mean'),
        Shipments=('Order ID', 'count')
    ).reset_index()

    state_df['Delay_Rate'] *= 100

    top_states = state_df.sort_values(by='Delay_Rate', ascending=False).head(5).copy()
    top_states.columns = ["State", "Delay %", "Shipments"]

    top_states["Delay %"] = top_states["Delay %"].round(1)
    top_states.insert(0, "Rank", range(1, len(top_states) + 1))

    # 🎨 Styling
    styled_states = top_states.style \
        .background_gradient(subset=["Delay %"], cmap="Reds") \
        .format({
            "Delay %": "{:.1f}%"
        }) \
        .set_properties(**{"text-align": "center"}) \
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]}
        ])

    st.dataframe(styled_states, use_container_width=True)
    
# ---------------- INSIGHTS ----------------
st.markdown("### 💡 Insights")

best = fastest.iloc[0]
avg_time = fastest["Avg Lead Time"].mean()
avg_delay = fastest["Delay %"].mean()

col1, col2 = st.columns(2)

with col1:
    st.success(f"""
    🚀 Best Route: {best['Route']}  
    ⏱ Avg Lead Time: {best['Avg Lead Time']} days
    """)

with col2:
    st.info(f"""
    📊 Avg Lead Time: {avg_time:.1f} days  
    ⚠ Avg Delay Rate: {avg_delay:.1f}%
    """)