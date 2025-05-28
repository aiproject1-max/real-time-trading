import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime
import time

st.set_page_config(page_title="Trading Dashboard", layout="wide")

# Init session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Time": pd.Series(dtype="str"),
        "Price": pd.Series(dtype="float")
    })

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Title
st.title("📈 Async-like Trading Dashboard")

# Simulate PnL
pnl = random.randint(-1000, 1000)
st.metric("Real-Time PnL", f"${pnl}")

# Generate new price point
now = datetime.now().strftime("%H:%M:%S")
price = 100 + random.uniform(-1, 1) + 0.1 * len(st.session_state.data)
new_row = pd.DataFrame({"Time": [now], "Price": [price]})

# Append safely
if not st.session_state.data.empty and not new_row.empty:
    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True).tail(100)
else:
    st.session_state.data = new_row

# Price chart
st.subheader("📊 Price Stream")
fig, ax = plt.subplots()
ax.plot(st.session_state.data["Time"], st.session_state.data["Price"], marker='o')
ax.set_xlabel("Time")
ax.set_ylabel("Price")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Non-blocking autorefresh every 1 second
if time.time() - st.session_state.last_update >= 1:
    st.session_state.last_update = time.time()
    st.experimental_rerun()
