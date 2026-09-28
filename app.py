import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fitness Track Insights",
    layout="wide"
)

# ---------------------------------------------------------
# COLOUR THEME
# ---------------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #F7F9FA;
}

.main-title {
    color: #263238;
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    color: #607D8B;
    font-size: 16px;
    margin-bottom: 25px;
}

.section-title {
    color: #263238;
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.metric-card {
    padding: 18px;
    border-radius: 14px;
    color: white;
    min-height: 120px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

.metric-title {
    font-size: 15px;
    font-weight: 600;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    margin-top: 12px;
}

.info-card {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E0E6E8;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
DATA_FOLDER = "data/cleaned"

daily = pd.read_csv(f"{DATA_FOLDER}/daily_master.csv")
sleep = pd.read_csv(f"{DATA_FOLDER}/sleep.csv")

daily["ActivityDate"] = pd.to_datetime(daily["ActivityDate"])
sleep["SleepDay"] = pd.to_datetime(sleep["SleepDay"])


# ---------------------------------------------------------
# ADDITIONAL VARIABLES
# ---------------------------------------------------------
daily["Weekday"] = daily["ActivityDate"].dt.day_name()

daily["ActiveMinutes"] = (
    daily["VeryActiveMinutes"]
    + daily["FairlyActiveMinutes"]
    + daily["LightlyActiveMinutes"]
)


def activity_level(minutes):
    if minutes >= 60:
        return "High"
    elif minutes >= 30:
        return "Moderate"
    else:
        return "Low"


daily["ActivityLevel"] = daily["ActiveMinutes"].apply(activity_level)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.markdown(
    '<div class="main-title">Fitness Track Insights Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive analysis of activity, calories, steps, sleep and daily behaviour</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Filters")

users = sorted(daily["Id"].unique())

selected_user = st.sidebar.selectbox(
    "User ID",
    ["All Users"] + list(users)
)

weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

selected_days = st.sidebar.multiselect(
    "Weekday",
    weekdays,
    default=weekdays
)

min_date = daily["ActivityDate"].min().date()
max_date = daily["ActivityDate"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

selected_activity = st.sidebar.selectbox(
    "Activity Level",
    ["All", "High", "Moderate", "Low"]
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------
filtered = daily.copy()

if selected_user != "All Users":
    filtered = filtered[filtered["Id"] == selected_user]

filtered = filtered[
    filtered["Weekday"].isin(selected_days)
]

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered = filtered[
        (filtered["ActivityDate"].dt.date >= start_date)
        & (filtered["ActivityDate"].dt.date <= end_date)
    ]

if selected_activity != "All":

    filtered = filtered[
        filtered["ActivityLevel"] == selected_activity
    ]


# ---------------------------------------------------------
# SLEEP FILTER
# ---------------------------------------------------------
filtered_sleep = sleep.copy()

if selected_user != "All Users":

    filtered_sleep = filtered_sleep[
        filtered_sleep["Id"] == selected_user
    ]

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    filtered_sleep = filtered_sleep[
        (filtered_sleep["SleepDay"].dt.date >= start_date)
        & (filtered_sleep["SleepDay"].dt.date <= end_date)
    ]


# ---------------------------------------------------------
# RECORD COUNT
# ---------------------------------------------------------
st.write(
    f"Showing {len(filtered):,} daily records after filters"
)


# ---------------------------------------------------------
# KEY METRICS
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Key Metrics</div>',
    unsafe_allow_html=True
)

if len(filtered) > 0:

    avg_steps = filtered["TotalSteps"].mean()
    avg_calories = filtered["Calories"].mean()
    avg_sedentary = filtered["SedentaryMinutes"].mean()
    avg_active = filtered["ActiveMinutes"].mean()

else:

    avg_steps = 0
    avg_calories = 0
    avg_sedentary = 0
    avg_active = 0


if len(filtered_sleep) > 0:
    avg_sleep = filtered_sleep["TotalMinutesAsleep"].mean() / 60
else:
    avg_sleep = 0


c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.markdown(f"""
    <div class="metric-card" style="background:#20AFAF;">
        <div class="metric-title">Average Steps</div>
        <div class="metric-value">{avg_steps:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="metric-card" style="background:#2689D9;">
        <div class="metric-title">Average Calories</div>
        <div class="metric-value">{avg_calories:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown(f"""
    <div class="metric-card" style="background:#FF7350;">
        <div class="metric-title">Sedentary Minutes</div>
        <div class="metric-value">{avg_sedentary:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)


with c4:

    st.markdown(f"""
    <div class="metric-card" style="background:#EF5B8D;">
        <div class="metric-title">Average Sleep</div>
        <div class="metric-value">{avg_sleep:.1f} hrs</div>
    </div>
    """, unsafe_allow_html=True)


with c5:

    st.markdown(f"""
    <div class="metric-card" style="background:#16A6A6;">
        <div class="metric-title">Active Minutes</div>
        <div class="metric-value">{avg_active:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# DAILY ACTIVITY TREND
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Daily Activity Trend</div>',
    unsafe_allow_html=True
)

if len(filtered) > 0:

    trend = (
        filtered.groupby("ActivityDate")
        .agg({
            "TotalSteps": "mean",
            "Calories": "mean"
        })
        .sort_index()
    )

    st.line_chart(trend)

else:

    st.info("No data available for the selected filters.")


# ---------------------------------------------------------
# ACTIVITY LEVEL
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Activity Level</div>',
    unsafe_allow_html=True
)

if len(filtered) > 0:

    activity_counts = (
        filtered["ActivityLevel"]
        .value_counts()
        .reindex(["High", "Moderate", "Low"])
        .fillna(0)
    )

    st.bar_chart(activity_counts)


# ---------------------------------------------------------
# ACTIVITY MINUTES
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Average Activity Minutes</div>',
    unsafe_allow_html=True
)

if len(filtered) > 0:

    activity_minutes = filtered[
        [
            "VeryActiveMinutes",
            "FairlyActiveMinutes",
            "LightlyActiveMinutes",
            "SedentaryMinutes"
        ]
    ].mean()

    st.bar_chart(activity_minutes)


# ---------------------------------------------------------
# SLEEP SUMMARY
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Sleep Summary</div>',
    unsafe_allow_html=True
)

if len(filtered_sleep) > 0:

    sleep_summary = (
        filtered_sleep[
            [
                "TotalMinutesAsleep",
                "TotalTimeInBed"
            ]
        ].mean() / 60
    )

    sleep_col1, sleep_col2 = st.columns(2)

    with sleep_col1:

        st.markdown(f"""
        <div class="info-card">
            <b>Average Sleep</b>
            <h2>{sleep_summary["TotalMinutesAsleep"]:.1f} hours</h2>
        </div>
        """, unsafe_allow_html=True)

    with sleep_col2:

        st.markdown(f"""
        <div class="info-card">
            <b>Average Time in Bed</b>
            <h2>{sleep_summary["TotalTimeInBed"]:.1f} hours</h2>
        </div>
        """, unsafe_allow_html=True)

else:

    st.info("No sleep records available for the selected filters.")


# ---------------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">Data Preview</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered,
    width="stretch",
    height=350
)
