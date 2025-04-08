import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load & Clean Data ---
# Read the CSV file
df = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")

# Convert 'Date' to datetime and drop rows with invalid dates
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(subset=['Date'], inplace=True)

# parsing the 'Time' column (assuming the format is "HH:MM:SS")
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
df.dropna(subset=['Time'], inplace=True)
df['Hour'] = df['Time'].dt.hour

df.info()
df

# Extract the day of the week from 'Date'
df['DayOfWeek'] = df['Date'].dt.day_name()
# Order the days in a natural week order
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)
df.info()
df['Time'].head(35)

# --- Visualization ---

# 1. Bar Plot: Accident Count by Day of the Week
day_counts = df['DayOfWeek'].value_counts().reindex(day_order)
plt.figure(figsize=(8, 5))
sns.barplot(x=day_counts.index, y=day_counts.values, palette="viridis")
plt.title("Accident Count by Day of the Week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.savefig("accidents_by_day.png")
plt.show()

# 2. Line Plot: Accident Count by Hour of the Day
hour_counts = df['Hour'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
sns.lineplot(x=hour_counts.index, y=hour_counts.values, marker="o")
plt.title("Accident Count by Hour of the Day")
plt.xlabel("Hour (0 - 23)")
plt.ylabel("Number of Accidents")
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()
plt.savefig("accidents_by_hour.png")
plt.show()

# 3. Heatmap: Accident Count by Day of Week vs. Hour of Day
# pivot table with days as rows and hours as columns
pivot = df.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Accident_Count')
pivot_table = pivot.pivot(index='DayOfWeek', columns='Hour', values='Accident_Count')
# Ensure row order follows Monday to Sunday
pivot_table = pivot_table.reindex(day_order)
# Fill missing values with 0
pivot_table = pivot_table.fillna(0)
pivot_table.sum
# normalizing each row to percentage (each day's total becomes 100%)
pivot_table_percent = pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12, 6))
sns.heatmap(pivot_table_percent, cmap="YlGnBu", annot=True, fmt=".1f", linewidths=0.5)
plt.title("Heatmap of Accident Percentages by Day of Week and Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week")
plt.tight_layout()
plt.savefig("heatmap_day_hour_percent.png")
plt.show()
