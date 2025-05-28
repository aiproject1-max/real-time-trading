import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import yfinance as yf
import asyncio
import time

st.set_page_config(page_title="Async Trading Dashboard", layout="wide")

# Initialize session state
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True
if "last_tnx_update" not in st.session_state:
    st.session_state.last_tnx_update = 0

st.title("📈 Async Trading Dashboard")

# Auto-refresh toggle
st.checkbox("🔄 Auto Refresh (every 10s)", key="auto_refresh")

# Fetch TNX (10Y Treasury Yield) real-time data
@st.cache_data(ttl=60)
def fetch_tnx_chart():
    tnx = yf.Ticker("^TNX")
    tnx_data = tnx.history(period="3d", interval="1m")
    tnx_data.reset_index(inplace=True)
    return tnx_data

# Fetch and plot
tnx_data = fetch_tnx_chart()

# Top Plot - Plotly
st.subheader("📊 CBOE 10-Year Treasury Yield (Real-Time, Plotly)")
fig_plotly = go.Figure()
fig_plotly.add_trace(go.Scatter(
    x=tnx_data["Datetime"],
    y=tnx_data["Close"],
    mode="lines+markers",
    line=dict(color="firebrick"),
    marker=dict(size=4),
    name="10Y Yield"
))
fig_plotly.update_layout(
    xaxis_title="Time",
    yaxis_title="Yield (%)",
    margin=dict(l=40, r=20, t=40, b=40),
    height=400,
)
st.plotly_chart(fig_plotly, use_container_width=True)

# Bottom Plot - Matplotlib
st.subheader("📉 Static Chart View (Matplotlib)")
fig_mpl, ax = plt.subplots()
ax.plot(tnx_data["Datetime"], tnx_data["Close"], marker="o", color="firebrick")
ax.set_xlabel("Time")
ax.set_ylabel("Yield (%)")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig_mpl)

# Async refresh
async def maybe_rerun():
    await asyncio.sleep(10)
    st.session_state.last_tnx_update = time.time()
    st.rerun()

# Trigger refresh
if st.session_state.auto_refresh:
    asyncio.run(maybe_rerun())
