import streamlit as st
import pandas as pd

st.set_page_config(page_title="Daily Activity", layout="wide")

DATA_FOLDER = "data/cleaned"
daily = pd.read_csv(f"{DATA_FOLDER}/daily_master.csv")

daily["ActivityDate"] = pd.to_datetime(daily["ActivityDate"])

st.title("Daily Activity Analysis")
st.write("Detailed analysis of daily steps, calories, distance and activity levels.")

# Sidebar filter
st.sidebar.header("Filters")

users = sorted(daily["Id"].unique())
selected_user = st.sidebar.selectbox("Select User", ["All Users"] + list(users))

if selected_user != "All Users":
    df = daily[daily["Id"] == selected_user].copy()
else:
    df = daily.copy()

# Metrics
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average Steps", f"{df['TotalSteps'].mean():,.0f}")
col2.metric("Average Calories", f"{df['Calories'].mean():,.0f}")
col3.metric("Average Distance", f"{df['TotalDistance'].mean():.2f} km")
col4.metric("Average Sedentary Minutes", f"{df['SedentaryMinutes'].mean():,.0f}")

# Steps trend
st.subheader("Steps Trend")

steps_chart = (
    df[["ActivityDate", "TotalSteps"]]
    .sort_values("ActivityDate")
    .set_index("ActivityDate")
)

st.line_chart(steps_chart)

# Calories trend
st.subheader("Calories Trend")

calories_chart = (
    df[["ActivityDate", "Calories"]]
    .sort_values("ActivityDate")
    .set_index("ActivityDate")
)

st.line_chart(calories_chart)

# Activity minutes
st.subheader("Activity Minutes")

activity = df[
    [
        "VeryActiveMinutes",
        "FairlyActiveMinutes",
        "LightlyActiveMinutes",
        "SedentaryMinutes"
    ]
].mean()

st.bar_chart(activity)

# Data table
st.subheader("Daily Activity Data")
st.dataframe(df, width="stretch")
