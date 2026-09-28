import streamlit as st
import pandas as pd

st.set_page_config(page_title="Weight Analysis", layout="wide")

DATA_FOLDER = "data/cleaned"

weight = pd.read_csv(f"{DATA_FOLDER}/weight.csv")

weight["Date"] = pd.to_datetime(weight["Date"])

st.title("Weight Analysis")
st.write("Analysis of weight measurements and changes over time.")

# Filters
st.sidebar.header("Filters")

users = sorted(weight["Id"].unique())

selected_user = st.sidebar.selectbox(
    "User ID",
    ["All Users"] + list(users)
)

if selected_user != "All Users":
    df = weight[weight["Id"] == selected_user].copy()
else:
    df = weight.copy()

# Metrics
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

avg_weight = df["WeightKg"].mean()
min_weight = df["WeightKg"].min()
max_weight = df["WeightKg"].max()

col1.metric("Average Weight", f"{avg_weight:.1f} kg")
col2.metric("Minimum Weight", f"{min_weight:.1f} kg")
col3.metric("Maximum Weight", f"{max_weight:.1f} kg")

# Weight trend
st.subheader("Weight Trend")

weight_trend = (
    df[["Date", "WeightKg"]]
    .sort_values("Date")
    .set_index("Date")
)

st.line_chart(weight_trend)

# Weight by user
st.subheader("Average Weight by User")

user_weight = (
    df.groupby("Id")["WeightKg"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(user_weight)

# BMI
if "BMI" in df.columns:

    st.subheader("BMI Analysis")

    bmi_data = df["BMI"].dropna()

    if len(bmi_data) > 0:

        bmi_col1, bmi_col2 = st.columns(2)

        bmi_col1.metric(
            "Average BMI",
            f"{bmi_data.mean():.1f}"
        )

        bmi_col2.metric(
            "BMI Records",
            f"{len(bmi_data):,}"
        )

        st.line_chart(
            df[["Date", "BMI"]]
            .dropna()
            .sort_values("Date")
            .set_index("Date")
        )

# Data
st.subheader("Weight Data")

st.dataframe(
    df,
    width="stretch"
)
