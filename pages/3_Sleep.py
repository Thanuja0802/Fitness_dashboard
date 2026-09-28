import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sleep Analysis", layout="wide")

DATA_FOLDER = "data/cleaned"
sleep = pd.read_csv(f"{DATA_FOLDER}/sleep.csv")

sleep["SleepDay"] = pd.to_datetime(sleep["SleepDay"])

st.title("Sleep Analysis")
st.write("Analysis of sleep duration and time spent in bed.")

# Filters
st.sidebar.header("Filters")

users = sorted(sleep["Id"].unique())

selected_user = st.sidebar.selectbox(
    "User ID",
    ["All Users"] + list(users)
)

if selected_user != "All Users":
    df = sleep[sleep["Id"] == selected_user].copy()
else:
    df = sleep.copy()

# Metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

avg_sleep = df["TotalMinutesAsleep"].mean() / 60
avg_bed = df["TotalTimeInBed"].mean() / 60
avg_awake = (df["TotalTimeInBed"] - df["TotalMinutesAsleep"]).mean()

col1.metric("Average Sleep", f"{avg_sleep:.1f} hrs")
col2.metric("Average Time in Bed", f"{avg_bed:.1f} hrs")
col3.metric("Average Awake Time", f"{avg_awake:.0f} min")

# Sleep trend
st.subheader("Sleep Trend")

sleep_trend = (
    df[["SleepDay", "TotalMinutesAsleep"]]
    .sort_values("SleepDay")
    .set_index("SleepDay")
)

sleep_trend["Sleep Hours"] = sleep_trend["TotalMinutesAsleep"] / 60

st.line_chart(sleep_trend["Sleep Hours"])

# Sleep vs time in bed
st.subheader("Sleep vs Time in Bed")

comparison = df[
    ["SleepDay", "TotalMinutesAsleep", "TotalTimeInBed"]
].copy()

comparison["Sleep Hours"] = comparison["TotalMinutesAsleep"] / 60
comparison["Time in Bed Hours"] = comparison["TotalTimeInBed"] / 60

comparison = comparison.set_index("SleepDay")

st.line_chart(
    comparison[["Sleep Hours", "Time in Bed Hours"]]
)

# User comparison
st.subheader("Average Sleep by User")

user_sleep = (
    df.groupby("Id")["TotalMinutesAsleep"]
    .mean()
    .sort_values(ascending=False)
    / 60
)

st.bar_chart(user_sleep)

# Data
st.subheader("Sleep Data")
st.dataframe(df, width="stretch")
