import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime
import asyncio

st.set_page_config(page_title="Trading Dashboard", layout="wide")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Time": pd.Series(dtype="str"),
        "Price": pd.Series(dtype="float")
    })

# Title
st.title("📈 Real-Time Trading Dashboard (Async Refresh)")

# Simulate PnL
pnl = random.randint(-1000, 1000)
st.metric(label="Current PnL", value=f"${pnl}")

# Simulate price feed
current_time = datetime.now().strftime("%H:%M:%S")
price = 100 + random.uniform(-1, 1) + 0.1 * len(st.session_state.data)
new_row = pd.DataFrame({"Time": [current_time], "Price": [price]})

# Append safely
if not st.session_state.data.empty and not new_row.empty:
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True).tail(100)
else:
    st.session_state.data = new_row

# Draw chart
st.subheader("📊 Price Stream")
fig, ax = plt.subplots()
ax.plot(st.session_state.data["Time"], st.session_state.data["Price"], marker="o")
ax.set_xlabel("Time")
ax.set_ylabel("Price")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Async autorefresh (wait 1 second then rerun)
async def auto_refresh():
    await asyncio.sleep(1)
    st.experimental_rerun()

# Trigger refresh
asyncio.run(auto_refresh())
