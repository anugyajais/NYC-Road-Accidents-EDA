import numpy as np
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt


data = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")

data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.dropna(subset=['Date'])

# Extract Month and Year 
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year

monthly_counts = data.groupby('Month').size().reset_index(name='Accident_Count')
monthly_counts.sort_values('Month', inplace=True)

# Percentage of accidents per month
total_accidents = monthly_counts['Accident_Count'].sum()
monthly_counts['Percentage'] = (monthly_counts['Accident_Count'] / total_accidents) * 100

print("Overall Monthly Accident Distribution:")
print(monthly_counts)

# Better visibility with 'turbo'
norm = plt.Normalize(monthly_counts['Accident_Count'].min(), monthly_counts['Accident_Count'].max())
colors = plt.cm.YlGnBu(norm(monthly_counts['Accident_Count']))

plt.figure(figsize=(10, 6))
bars = plt.bar(monthly_counts['Month'].astype(str), monthly_counts['Percentage'], color=colors)
plt.title("Overall: Percentage of Accidents per Month from 2021-23")
plt.xlabel("Month")
plt.ylabel("Percentage of Total Accidents (%)")
plt.xticks(range(0, 12), [str(i+1) for i in range(12)])
plt.tight_layout()
plt.savefig("overall_monthly_accident_distribution.png")
print("Overall plot saved as 'overall_monthly_accident_distribution.png'.")
plt.show()

# -----------------------------x-----------------------------------x----------------------------------------

monthly_year = data.groupby(['Year', 'Month']).size().reset_index(name='Accident_Count')
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
    colors_year = plt.cm.YlGnBu(norm_year(df_year['Accident_Count']))  # Visually stronger

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
