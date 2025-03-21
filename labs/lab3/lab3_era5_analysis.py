import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Files
berlin_file = '../../datasets/berlin_era5_wind_20241231_20241231.csv'
munich_file = '../../datasets/munich_era5_wind_20241231_20241231.csv'


# Loading the data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=["timestamp"])
        print(f"{file_path} is loaded.")
        print("\nData info:", df.info())
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

#calculate the wind speed
def calculate_wind_speed(df):
    df["wind_speed"] = np.sqrt(df["u10m"] ** 2 + df["v10m"] ** 2)
    return df


# seasonal and monthly averages.
def compute_aggregations(df):
    df["month"] = df["timestamp"].dt.month
    df["season"] = df["timestamp"].dt.month % 12 // 3 + 1  # 1: Winter, 2: Spring, 3: Summer, 4: Fall
    monthly_avg = df.groupby("month")["wind_speed"].mean()
    seasonal_avg = df.groupby("season")["wind_speed"].mean()
    return monthly_avg, seasonal_avg


# Visualization
def plot_wind_speed_trends(berlin_df, munich_df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=berlin_df["timestamp"], y=berlin_df["wind_speed"], label="Berlin")
    sns.lineplot(x=munich_df["timestamp"], y=munich_df["wind_speed"], label="Munich")
    plt.xlabel("Date")
    plt.ylabel("Wind Speed (m/s)")
    plt.title("Berlin ve Munich Monthly Wind Speed Trends ")
    plt.legend()
    plt.show()


#Main Code
berlin_df = load_data(berlin_file)
munich_df = load_data(munich_file)

if berlin_df is not None and munich_df is not None:
    berlin_df = calculate_wind_speed(berlin_df)
    munich_df = calculate_wind_speed(munich_df)

    berlin_monthly, berlin_seasonal = compute_aggregations(berlin_df)
    munich_monthly, munich_seasonal = compute_aggregations(munich_df)

    print("Berlin Monthly averages:\n", berlin_monthly)
    print("Berlin Seasonal averages:\n", berlin_seasonal)
    print("Munich Monthly averages:\n", munich_monthly)
    print("Munich Seasonal averages:\n", munich_seasonal)

    plot_wind_speed_trends(berlin_df, munich_df)
