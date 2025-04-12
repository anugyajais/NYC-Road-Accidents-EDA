"""
1. **Monthly Accident Distribution Analysis:**  
   Assess the percentage of total accidents per month to identify seasonal trends and potential outliers.
"""

import textwrap
import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

# Define a uniform colormap and select specific shades for single-color plots
cmap = plt.get_cmap("YlGnBu")
single_color = cmap(0.6)    # Used for plots needing a single color
lighter_color = cmap(0.4)   # Used for secondary elements when needed
darker_color = cmap(0.8)    # Used for contrast in dual-colored plots

# --- Data Loading and Initial Cleaning (used across all objectives) ---
df = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(subset=['Date'], inplace=True)

# Parse 'Time' column (assuming the format is "HH:MM:SS") and extract hour
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce')
df.dropna(subset=['Time'], inplace=True)
df['Hour'] = df['Time'].dt.hour

# Extract Month and Year for time series analyses
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# ------------------ Objective 1: Monthly Accident Distribution Analysis ------------------ 

monthly_counts = df.groupby('Month').size().reset_index(name='Accident_Count')
monthly_counts.sort_values('Month', inplace=True)

# Percentage of accidents per month
total_accidents = monthly_counts['Accident_Count'].sum()
monthly_counts['Percentage'] = (monthly_counts['Accident_Count'] / total_accidents) * 100

print("Overall Monthly Accident Distribution:")
print(monthly_counts)

# Use uniform colormap "YlGnBu" for visualization
norm = plt.Normalize(monthly_counts['Accident_Count'].min(), monthly_counts['Accident_Count'].max())
colors = plt.cm.YlGnBu(norm(monthly_counts['Accident_Count']))

plt.figure(figsize=(10, 6))
plt.bar(monthly_counts['Month'].astype(str), monthly_counts['Percentage'], color=colors)
plt.title("Overall: Percentage of Accidents per Month from 2021-23")
plt.xlabel("Month")
plt.ylabel("Percentage of Total Accidents (%)")
plt.xticks(range(0, 12), [str(i+1) for i in range(12)])
plt.tight_layout()
plt.savefig("overall_monthly_accident_distribution.png")
print("Overall plot saved as 'overall_monthly_accident_distribution.png'.")
plt.show()

# Grouping by Year and Month for yearly breakdown
monthly_year = df.groupby(['Year', 'Month']).size().reset_index(name='Accident_Count')
monthly_year.sort_values(['Year', 'Month'], inplace=True)
monthly_year['Percentage'] = monthly_year.groupby('Year')['Accident_Count'].transform(lambda x: (x / x.sum()) * 100)

print("Monthly Accident Distribution by Year:")
print(monthly_year)

years = sorted(monthly_year['Year'].unique())
fig, axes = plt.subplots(nrows=len(years), ncols=1, figsize=(10, 6 * len(years)))
if len(years) == 1:
    axes = [axes]

for ax, year in zip(axes, years):
    df_year = monthly_year[monthly_year['Year'] == year].sort_values('Month')
    
    norm_year = plt.Normalize(df_year['Accident_Count'].min(), df_year['Accident_Count'].max())
    colors_year = plt.cm.YlGnBu(norm_year(df_year['Accident_Count']))

    ax.bar(df_year['Month'].astype(str), df_year['Percentage'], color=colors_year)
    ax.set_title(f"Year {year}: Percentage of Accidents per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Percentage of Total Accidents (%)")
    ax.set_xticks(range(0, 12))
    ax.set_xticklabels([str(i+1) for i in range(12)])

    sm = plt.cm.ScalarMappable(cmap="YlGnBu", norm=norm_year)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Accident Count")

plt.tight_layout()
plt.savefig('monthly_accident_distribution_by_year.png')
print("Yearly plots saved as 'monthly_accident_distribution_by_year.png'.")
plt.show()

"""
2. **Temporal Pattern Decomposition:**  
   Break down accident frequencies by day of the week and hour of the day to pinpoint peak periods of incidents.
"""

# Extract the day of the week from 'Date'
df['DayOfWeek'] = df['Date'].dt.day_name()
# Order the days in a natural week order
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['DayOfWeek'] = pd.Categorical(df['DayOfWeek'], categories=day_order, ordered=True)
df.info()  # Display dataframe info for verification

# --- Visualization ---

# 1. Bar Plot: Accident Count by Day of the Week using uniform palette
day_counts = df['DayOfWeek'].value_counts().reindex(day_order)
plt.figure(figsize=(8, 5))
sns.barplot(x=day_counts.index, y=day_counts.values, palette="YlGnBu")
plt.title("Accident Count by Day of the Week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.savefig("accidents_by_day.png")
plt.show()

# 2. Line Plot: Accident Count by Hour of the Day using a single uniform color
hour_counts = df['Hour'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
sns.lineplot(x=hour_counts.index, y=hour_counts.values, marker="o", color=single_color)
plt.title("Accident Count by Hour of the Day")
plt.xlabel("Hour (0 - 23)")
plt.ylabel("Number of Accidents")
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()
plt.savefig("accidents_by_hour.png")
plt.show()

# 3. Heatmap: Accident Count by Day of Week vs. Hour of Day using uniform cmap
pivot = df.groupby(['DayOfWeek', 'Hour']).size().reset_index(name='Accident_Count')
pivot_table = pivot.pivot(index='DayOfWeek', columns='Hour', values='Accident_Count')
pivot_table = pivot_table.reindex(day_order).fillna(0)
# Normalize each row to percentage (each day's total becomes 100%)
pivot_table_percent = pivot_table.div(pivot_table.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12, 6))
sns.heatmap(pivot_table_percent, cmap="YlGnBu", annot=True, fmt=".1f", linewidths=0.5)
plt.title("Heatmap of Accident Percentages by Day of Week and Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week")
plt.tight_layout()
plt.savefig("heatmap_day_hour_percent.png")
plt.show()

"""
3. **Accident Hotspot Identification:**  
   Identify areas with higher concentrations of accidents using available location data (e.g., by borough and street name).
"""

# Clean location columns: fill missing values with 'Unknown'
df['Borough'] = df['Borough'].fillna('Unknown')
df['Street Name'] = df['Street Name'].fillna('Unknown')

hotspots = df.groupby(['Borough', 'Street Name']).size().reset_index(name='Accident_Count')
top_hotspots = hotspots.sort_values('Accident_Count', ascending=False).head(20)

plt.figure(figsize=(12, 8))
# Use uniform palette for categorical differentiation by Borough
sns.barplot(data=top_hotspots, y='Street Name', x='Accident_Count', hue='Borough', palette="YlGnBu", dodge=False)
plt.title("Top 20 Accident Hotspots by Street and Borough")
plt.xlabel("Number of Accidents")
plt.ylabel("Street Name")
plt.tight_layout()
plt.savefig("accident_hotspots.png")
plt.show()

"""
4. **Street-Specific Risk Evaluation:**  
   Determine which street experiences the highest number of accidents and calculate its share relative to the total.
"""

# (Note: 'Street Name' has already been filled with 'Unknown' in the previous section)
total_accidents = df.shape[0]
street_counts = df['Street Name'].value_counts()
top_street = street_counts.idxmax()
top_accident_count = street_counts.max()
share_percentage = (top_accident_count / total_accidents) * 100

print("Street-Specific Risk Evaluation:")
print(f"Street with highest accidents: {top_street}")
print(f"Number of accidents on {top_street}: {top_accident_count}")
print(f"Share of total accidents: {share_percentage:.2f}%")

# --- Weekly Average Calculation ---
df['Week'] = df['Date'].dt.to_period('W').apply(lambda r: r.start_time)
weekly_counts = df.groupby(['Street Name', 'Week']).size().reset_index(name='Weekly_Count')
weekly_avg = weekly_counts.groupby('Street Name')['Weekly_Count'].mean()

# --- Visualization ---
top10_streets = street_counts.head(10)
short_street_names = [textwrap.shorten(name, width=15, placeholder="...") for name in top10_streets.index]

plt.figure(figsize=(12, 7))
ax = top10_streets.plot(kind='bar', color=single_color)

ax.set_xticklabels(short_street_names, rotation=30, ha='right')
plt.title("Top 10 Streets by Accident Count\n(with Average Weekly Accidents)")
plt.xlabel("Street Name")
plt.ylabel("Total Accident Count")
plt.subplots_adjust(bottom=0.25, top=0.85)

for i, street in enumerate(top10_streets.index):
    bar = ax.patches[i]
    avg_weekly_val = weekly_avg.get(street, 0)
    bar_height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, bar_height + 30,
            f"{avg_weekly_val:.1f} / week",
            ha='center', va='bottom', fontsize=9, color='black')

plt.tight_layout()
plt.savefig("top_streets_with_weekly_avg.png")
plt.show()

"""
5. **Contributing Factor Assessment:**  
   Analyze the most common contributing factors for all accidents, providing insights into underlying causes.
"""

df['Contributing Factor'] = df['Contributing Factor'].fillna('Unknown')

cf_counts = df['Contributing Factor'].value_counts()
unspecified_count = cf_counts.get("Unspecified", 0)
cf_counts_filtered = cf_counts.drop("Unspecified", errors='ignore')
specified_count = cf_counts_filtered.sum()

plt.figure(figsize=(10, 7))
top_factors = cf_counts_filtered.head(10)
ax = sns.barplot(
    x=top_factors.values,
    y=top_factors.index,
    palette="YlGnBu",
    hue=None,
    legend=False
)

plt.title("Top 10 Contributing Factors for Accidents", fontsize=15)
plt.xlabel("Number of Accidents", fontsize=13)
plt.ylabel("Contributing Factor", fontsize=13)
max_val = max(top_factors.values)
plt.xlim(0, max_val * 1.1)

for p in ax.patches:
    width = p.get_width()
    ax.text(width + max_val * 0.01,
            p.get_y() + p.get_height() / 2,
            f"{int(width)}",
            ha='left', va='center', fontsize=11, color='black')

plt.figtext(0.5, 0.01,
            f"Total accidents with 'Unspecified': {unspecified_count} | Total with specified factors: {specified_count}",
            wrap=True, horizontalalignment='center', fontsize=12, color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("top_contributing_factors_with_weekly_avg.png")
plt.show()

"""
6. **Fatal Accident Causality Analysis:**  
   Isolate and analyze fatal accidents to determine the primary contributing factors in these cases.
								AND
7. **Injury Severity Profiling:**  
   Evaluate the distribution of injuries and fatalities among pedestrians, cyclists, and motorists to assess public safety risks.
"""

# Ensure numeric columns are numeric; convert and fill NaN with 0
numeric_cols = ['Persons Killed', 'Pedestrians Killed', 'Cyclists Killed', 'Motorists Killed',
                'Pedestrians Injured', 'Cyclists Injured', 'Motorists Injured']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# --- Objective 6: Fatal Accident Causality Analysis ---
df['Total Fatalities'] = (df['Persons Killed'] + 
                          df['Pedestrians Killed'] + 
                          df['Cyclists Killed'] + 
                          df['Motorists Killed'])
fatal_df = df[df['Total Fatalities'] > 0]
fatal_cf_counts = fatal_df['Contributing Factor'].value_counts()

plt.figure(figsize=(10, 6))
ax1 = sns.barplot(x=fatal_cf_counts.head(10).values, 
                  y=fatal_cf_counts.head(10).index, 
                  palette="YlGnBu", 
                  hue=None, legend=False)
plt.title("Top Contributing Factors in Fatal Accidents", fontsize=15)
plt.xlabel("Number of Fatal Accidents", fontsize=13)
plt.ylabel("Contributing Factor", fontsize=13)
max_val = fatal_cf_counts.head(10).max()
plt.xlim(0, max_val * 1.1)
for p in ax1.patches:
    width = p.get_width()
    ax1.text(width + 0.01 * max_val,
             p.get_y() + p.get_height() / 2,
             f"{int(width)}",
             ha='left', va='center', fontsize=11, color='black')
plt.tight_layout()
plt.savefig("fatal_accident_causality.png")
plt.show()

# --- Objective 7: Injury Severity Profiling ---
ped_injured = df['Pedestrians Injured'].sum()
ped_killed  = df['Pedestrians Killed'].sum()
cycl_injured = df['Cyclists Injured'].sum()
cycl_killed  = df['Cyclists Killed'].sum()
motor_injured = df['Motorists Injured'].sum()
motor_killed  = df['Motorists Killed'].sum()

injury_data = {
    "Category": ["Pedestrians", "Cyclists", "Motorists"],
    "Injured": [ped_injured, cycl_injured, motor_injured],
    "Killed": [ped_killed, cycl_killed, motor_killed]
}
injury_df = pd.DataFrame(injury_data)

plt.figure(figsize=(8, 6))
categories = injury_df["Category"]
injured = injury_df["Injured"]
killed = injury_df["Killed"]
width = 0.6

# For uniformity, select two shades from the YlGnBu colormap
bars_injured = plt.bar(categories, injured, width=width, label="Injured", color=lighter_color)
bars_killed = plt.bar(categories, killed, width=width, bottom=injured, label="Killed", color=darker_color)

plt.title("Injury Severity Profiling", fontsize=15)
plt.xlabel("Category", fontsize=13)
plt.ylabel("Total Count", fontsize=13)
plt.legend()

for bar in bars_injured:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height / 2,
             f"{int(height)}", ha="center", va="center", fontsize=11, color='black')

for bar, base in zip(bars_killed, injured):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, base + height / 2,
             f"{int(height)}", ha="center", va="center", fontsize=11, color='black')

plt.tight_layout()
plt.savefig("injury_severity_stacked.png")
plt.show()

"""
10. **Data Quality and Outlier Management:**  
    Implement robust data cleaning and outlier detection techniques to ensure the reliability of the insights derived.
"""

df['Persons Injured'] = pd.to_numeric(df['Persons Injured'], errors='coerce').fillna(0)

plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Persons Injured'], color=single_color)
plt.title("Boxplot of Persons Injured (Before Outlier Removal)")
plt.xlabel("Persons Injured")
plt.tight_layout()
plt.savefig("boxplot_before_outliers.png")
plt.show()

Q1 = df['Persons Injured'].quantile(0.25)
Q3 = df['Persons Injured'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['Persons Injured'] < lower_bound) | (df['Persons Injured'] > upper_bound)]
print(f"Number of outliers in 'Persons Injured': {outliers.shape[0]}")
df_clean = df[(df['Persons Injured'] >= lower_bound) & (df['Persons Injured'] <= upper_bound)]

plt.figure(figsize=(10, 6))
sns.boxplot(x=df_clean['Persons Injured'], color=single_color)
plt.title("Boxplot of Persons Injured (After Outlier Removal)")
plt.xlabel("Persons Injured")
plt.tight_layout()
plt.savefig("boxplot_after_outliers.png")
plt.show()

print("Summary statistics before outlier removal:")
print(df['Persons Injured'].describe())
print("\nSummary statistics after outlier removal:")
print(df_clean['Persons Injured'].describe())
