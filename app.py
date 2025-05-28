import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime
import asyncio
import time

st.set_page_config(page_title="Async Trading Dashboard", layout="wide")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Time": pd.Series(dtype="str"),
        "Price": pd.Series(dtype="float")
    })

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

st.title("📈 Async Trading Dashboard")

# Toggle for auto refresh
st.checkbox("🔄 Auto Refresh (async, 1s)", key="auto_refresh")

# Simulated PnL
pnl = random.randint(-1000, 1000)
st.metric("Real-Time PnL", f"${pnl}")

# Simulate price
now = datetime.now().strftime("%H:%M:%S")
price = 100 + random.uniform(-1, 1) + 0.1 * len(st.session_state.data)
new_row = pd.DataFrame({"Time": [now], "Price": [price]})

if not st.session_state.data.empty and not new_row.empty:
    st.session_state.data = pd.concat(
        [st.session_state.data, new_row], ignore_index=True
    ).tail(100)
else:
    st.session_state.data = new_row

# Chart
st.subheader("📊 Price Stream")
fig, ax = plt.subplots()
ax.plot(st.session_state.data["Time"], st.session_state.data["Price"], marker="o")
ax.set_xlabel("Time")
ax.set_ylabel("Price")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Async refresh using asyncio.sleep inside a coroutine
async def maybe_rerun():
    await asyncio.sleep(1)
    st.session_state.last_update = time.time()
    st.rerun()

# Trigger coroutine conditionally
if st.session_state.auto_refresh:
    # This will run asynchronously and rerun after 1 second
    asyncio.run(maybe_rerun())
