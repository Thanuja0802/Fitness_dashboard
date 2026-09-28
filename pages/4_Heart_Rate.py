import streamlit as st
import pandas as pd

st.set_page_config(page_title="Heart Rate Analysis", layout="wide")

DATA_FOLDER = "data/cleaned"

heart = pd.read_csv(f"{DATA_FOLDER}/heart_rate.csv")

heart["Time"] = pd.to_datetime(heart["Time"])

# Create date and hour
heart["Date"] = heart["Time"].dt.date
heart["Hour"] = heart["Time"].dt.hour

st.title("Heart Rate Analysis")
st.write("Analysis of heart-rate patterns across users and time.")

# Filters
st.sidebar.header("Filters")

users = sorted(heart["Id"].unique())

selected_user = st.sidebar.selectbox(
    "User ID",
    ["All Users"] + list(users)
)

if selected_user != "All Users":
    df = heart[heart["Id"] == selected_user].copy()
else:
    df = heart.copy()

# Metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

avg_hr = df["Value"].mean()
min_hr = df["Value"].min()
max_hr = df["Value"].max()

col1.metric("Average Heart Rate", f"{avg_hr:.0f} bpm")
col2.metric("Minimum Heart Rate", f"{min_hr:.0f} bpm")
col3.metric("Maximum Heart Rate", f"{max_hr:.0f} bpm")

# Daily heart rate
st.subheader("Daily Average Heart Rate")

daily_hr = (
    df.groupby("Date")["Value"]
    .mean()
    .sort_index()
)

st.line_chart(daily_hr)

# Hourly heart rate
st.subheader("Average Heart Rate by Hour")

hourly_hr = (
    df.groupby("Hour")["Value"]
    .mean()
    .sort_index()
)

st.line_chart(hourly_hr)

# Distribution
st.subheader("Heart Rate Distribution")

hr_distribution = (
    df["Value"]
    .value_counts()
    .sort_index()
)

st.bar_chart(hr_distribution)

# User comparison
st.subheader("Average Heart Rate by User")

user_hr = (
    df.groupby("Id")["Value"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(user_hr)

# Preview
st.subheader("Heart Rate Data Preview")

st.dataframe(
    df.head(5000),
    width="stretch"
)
