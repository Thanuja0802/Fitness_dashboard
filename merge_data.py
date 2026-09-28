import pandas as pd
import os

data_folder = "data"

print("Creating master datasets...")

# ---------------- DAILY ----------------
daily = pd.read_csv(f"{data_folder}/dailyActivity_merged.csv")
daily["ActivityDate"] = pd.to_datetime(daily["ActivityDate"])

daily.to_csv(f"{data_folder}/daily_master.csv", index=False)
print("? daily_master.csv created:", len(daily), "rows")


# ---------------- HOURLY ----------------
hourly_cal = pd.read_csv(f"{data_folder}/hourlyCalories_merged.csv")
hourly_int = pd.read_csv(f"{data_folder}/hourlyIntensities_merged.csv")
hourly_steps = pd.read_csv(f"{data_folder}/hourlySteps_merged.csv")

hourly = hourly_cal.merge(
    hourly_int,
    on=["Id", "ActivityHour"],
    how="outer"
)

hourly = hourly.merge(
    hourly_steps,
    on=["Id", "ActivityHour"],
    how="outer"
)

hourly["ActivityHour"] = pd.to_datetime(hourly["ActivityHour"])

hourly.to_csv(f"{data_folder}/hourly_master.csv", index=False)
print("? hourly_master.csv created:", len(hourly), "rows")


# ---------------- MINUTE ----------------
minute_cal = pd.read_csv(f"{data_folder}/minuteCaloriesNarrow_merged.csv")
minute_int = pd.read_csv(f"{data_folder}/minuteIntensitiesNarrow_merged.csv")
minute_met = pd.read_csv(f"{data_folder}/minuteMETsNarrow_merged.csv")
minute_steps = pd.read_csv(f"{data_folder}/minuteStepsNarrow_merged.csv")

minute = minute_cal.merge(
    minute_int,
    on=["Id", "ActivityMinute"],
    how="outer"
)

minute = minute.merge(
    minute_met,
    on=["Id", "ActivityMinute"],
    how="outer"
)

minute = minute.merge(
    minute_steps,
    on=["Id", "ActivityMinute"],
    how="outer"
)

minute["ActivityMinute"] = pd.to_datetime(minute["ActivityMinute"])

minute.to_csv(f"{data_folder}/minute_master.csv", index=False)
print("? minute_master.csv created:", len(minute), "rows")


# ---------------- SLEEP ----------------
sleep = pd.read_csv(f"{data_folder}/sleepDay_merged.csv")
sleep["SleepDay"] = pd.to_datetime(sleep["SleepDay"])

sleep.to_csv(f"{data_folder}/sleep.csv", index=False)
print("? sleep.csv created:", len(sleep), "rows")


# ---------------- WEIGHT ----------------
weight = pd.read_csv(f"{data_folder}/weightLogInfo_merged.csv")
weight["Date"] = pd.to_datetime(weight["Date"])

weight.to_csv(f"{data_folder}/weight.csv", index=False)
print("? weight.csv created:", len(weight), "rows")


# ---------------- HEART RATE ----------------
heart_rate = pd.read_csv(f"{data_folder}/heartrate_seconds_merged.csv")
heart_rate["Time"] = pd.to_datetime(heart_rate["Time"])

heart_rate.to_csv(f"{data_folder}/heart_rate.csv", index=False)
print("? heart_rate.csv created:", len(heart_rate), "rows")


print("\nALL MASTER DATASETS CREATED SUCCESSFULLY!")
