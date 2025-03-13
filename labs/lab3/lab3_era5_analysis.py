import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes
import numpy as np

# 1. Load and Explore the Datasets
def load_data(file_path):
    try:
        df = pd.read_csv(file_path, parse_dates=['timestamp'])
        print(f"\nDataset loaded: {file_path}")
        print(f"Dataset Statistics:\n{df.describe()}\n")  # Display statistics
        return df
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return None

# File paths
file_path_berlin = "../../datasets/berlin_era5_wind_20241231_20241231.csv"
file_path_munich = "../../datasets/munich_era5_wind_20241231_20241231.csv"

# Load data
berlin = load_data(file_path_berlin)
munich = load_data(file_path_munich)

# Handle missing values
berlin.dropna(inplace=True)
munich.dropna(inplace=True)

# 2. Compute Temporal Aggregations
def calculate_wind_speed(df):
    df['wind_speed'] = (df['u10m']**2 + df['v10m']**2)**0.5
    df['wind_direction'] = np.arctan2(df['u10m'], df['v10m']) * 180 / np.pi
    df['wind_direction'] = (df['wind_direction'] + 360) % 360  # Ensure direction is between 0-360°
    return df

berlin = calculate_wind_speed(berlin)
munich = calculate_wind_speed(munich)

# Function to compute monthly and seasonal averages for wind speed & temperature
def compute_aggregations(df):
    df['year_month'] = df['timestamp'].dt.to_period('M')
    df['season'] = df['timestamp'].dt.month % 12 // 3 + 1  # 1=Winter, 2=Spring, etc.

    # Compute averages
    monthly_avg_wind = df.groupby('year_month')['wind_speed'].mean()
    seasonal_avg_wind = df.groupby('season')['wind_speed'].mean()

    if 't2m' in df.columns:  # Check if temperature data exists
        monthly_avg_temp = df.groupby('year_month')['t2m'].mean()
        seasonal_avg_temp = df.groupby('season')['t2m'].mean()
    else:
        monthly_avg_temp = None
        seasonal_avg_temp = None

    return monthly_avg_wind, seasonal_avg_wind, monthly_avg_temp, seasonal_avg_temp

# Compute for Berlin & Munich
berlin_monthly_avg_wind, berlin_seasonal_avg_wind, berlin_monthly_avg_temp, berlin_seasonal_avg_temp = compute_aggregations(berlin)
munich_monthly_avg_wind, munich_seasonal_avg_wind, munich_monthly_avg_temp, munich_seasonal_avg_temp = compute_aggregations(munich)

# Display Monthly & Seasonal Averages
print("\n📌 Monthly Average Wind Speeds (m/s):")
print("Berlin:\n", berlin_monthly_avg_wind)
print("Munich:\n", munich_monthly_avg_wind)

if berlin_monthly_avg_temp is not None and munich_monthly_avg_temp is not None:
    print("\n📌 Monthly Average Temperatures (°C):")
    print("Berlin:\n", berlin_monthly_avg_temp)
    print("Munich:\n", munich_monthly_avg_temp)

print("\n📌 Seasonal Average Wind Speeds (m/s):")
print("Berlin:\n", berlin_seasonal_avg_wind)
print("Munich:\n", munich_seasonal_avg_wind)

if berlin_seasonal_avg_temp is not None and munich_seasonal_avg_temp is not None:
    print("\n📌 Seasonal Average Temperatures (°C):")
    print("Berlin:\n", berlin_seasonal_avg_temp)
    print("Munich:\n", munich_seasonal_avg_temp)

# 3. Visualizations

# Time Series Plot of Monthly Average Wind Speeds
def plot_monthly_avg(berlin_monthly_avg, munich_monthly_avg):
    plt.figure(figsize=(10, 6))
    plt.plot(berlin_monthly_avg.index.astype(str), berlin_monthly_avg.values, label='Berlin', color='blue', marker='o')
    plt.plot(munich_monthly_avg.index.astype(str), munich_monthly_avg.values, label='Munich', color='red', marker='x')
    plt.title('Monthly Average Wind Speeds')
    plt.xlabel('Month')
    plt.ylabel('Wind Speed (m/s)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Seasonal Comparison Bar Charts
def plot_seasonal_comparison(berlin_seasonal_avg, munich_seasonal_avg):
    seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
    
    plt.figure(figsize=(10, 6))
    plt.bar(seasons, berlin_seasonal_avg.values, width=0.4, label='Berlin', align='center', color='blue')
    plt.bar(seasons, munich_seasonal_avg.values, width=0.4, label='Munich', align='edge', color='red')
    plt.title('Seasonal Comparison of Wind Speeds')
    plt.ylabel('Wind Speed (m/s)')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Wind Rose Diagrams (Directional Analysis)
def plot_wind_rose(df, location_name):
    windrose = WindroseAxes.from_ax()
    windrose.bar(df['wind_direction'], df['wind_speed'], bins=8, edgecolor='black')
    windrose.set_title(f'Wind Rose for {location_name}')
    plt.show()

# Display results for Berlin
plot_monthly_avg(berlin_monthly_avg_wind, munich_monthly_avg_wind)
plot_seasonal_comparison(berlin_seasonal_avg_wind, munich_seasonal_avg_wind)
plot_wind_rose(berlin, "Berlin")

# Display results for Munich
plot_wind_rose(munich, "Munich")


# Skyrim repository provides faster and easier usage for larger-scaled predictions. Additionally, it allows us to run computationally intensive weather forecasts on a personal computer thanks to its weather model with a consumer grade GPU.
