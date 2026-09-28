import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hourly Activity", layout="wide")

DATA_FOLDER = "data/cleaned"
hourly = pd.read_csv(f"{DATA_FOLDER}/hourly_master.csv")

hourly["ActivityHour"] = pd.to_datetime(hourly["ActivityHour"])

st.title("Hourly Activity Analysis")
st.write("Analysis of activity patterns throughout the day.")

# Sidebar
st.sidebar.header("Filters")

users = sorted(hourly["Id"].unique())
selected_user = st.sidebar.selectbox("Select User", ["All Users"] + list(users))

if selected_user != "All Users":
    df = hourly[hourly["Id"] == selected_user].copy()
else:
    df = hourly.copy()

# Extract hour
df["Hour"] = df["ActivityHour"].dt.hour

# Metrics
st.subheader("Hourly Activity Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Average Steps / Hour", f"{df['StepTotal'].mean():,.0f}")
col2.metric("Average Calories / Hour", f"{df['Calories'].mean():,.0f}")
col3.metric("Average Intensity", f"{df['TotalIntensity'].mean():.1f}")

# Steps by hour
st.subheader("Average Steps by Hour")

steps_by_hour = (
    df.groupby("Hour")["StepTotal"]
    .mean()
    .rename("Average Steps")
)

st.line_chart(steps_by_hour)

# Calories by hour
st.subheader("Average Calories by Hour")

calories_by_hour = (
    df.groupby("Hour")["Calories"]
    .mean()
    .rename("Average Calories")
)

st.line_chart(calories_by_hour)

# Intensity by hour
st.subheader("Average Intensity by Hour")

intensity_by_hour = (
    df.groupby("Hour")["TotalIntensity"]
    .mean()
    .rename("Average Intensity")
)

st.bar_chart(intensity_by_hour)

# Data
st.subheader("Hourly Activity Data")
st.dataframe(df, width="stretch")
