import pandas as pd
import os

data_folder = "data"
output_folder = os.path.join(data_folder, "cleaned")
os.makedirs(output_folder, exist_ok=True)

files = {
    "daily_master.csv": ["ActivityDate"],
    "hourly_master.csv": ["ActivityHour"],
    "minute_master.csv": ["ActivityMinute"],
    "sleep.csv": ["SleepDay"],
    "weight.csv": ["Date"],
    "heart_rate.csv": ["Time"]
}

print("=" * 60)
print("STARTING DATA CLEANING")
print("=" * 60)

for filename, date_columns in files.items():

    print("\nCleaning:", filename)

    input_path = os.path.join(data_folder, filename)
    output_path = os.path.join(output_folder, filename)

    df = pd.read_csv(input_path)

    rows_before = len(df)

    # Convert date/time columns
    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            format="mixed",
            errors="coerce"
        )

        invalid_dates = df[column].isna().sum()
        if invalid_dates > 0:
            print(f"Invalid dates in {column}:", invalid_dates)

    # Remove exact duplicate rows only
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Keep missing weight Fat values as missing
    if filename == "weight.csv":
        print("Missing Fat values retained:", df["Fat"].isna().sum())

    # Save cleaned copy
    df.to_csv(output_path, index=False)

    print("Rows before:", rows_before)
    print("Duplicate rows removed:", duplicates)
    print("Rows after:", len(df))
    print("Saved to:", output_path)

print("\n" + "=" * 60)
print("CLEANING COMPLETE")
print("Cleaned files are in the data/cleaned folder.")
print("=" * 60)
