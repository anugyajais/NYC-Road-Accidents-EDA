import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# --- Load & Clean Data ---
df = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")

# Fill missing 'Street Name' values
df['Street Name'] = df['Street Name'].fillna('Unknown')

# Convert 'Date' to datetime and drop invalid
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df.dropna(subset=['Date'], inplace=True)

# --- Street-Specific Risk Evaluation ---
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
# Get top 10 street names and truncate long ones for labels
top10_streets = street_counts.head(10)
short_street_names = [textwrap.shorten(name, width=15, placeholder="...") for name in top10_streets.index]

plt.figure(figsize=(12, 7))
ax = top10_streets.plot(kind='bar', color='skyblue')

# Set axis labels and title
ax.set_xticklabels(short_street_names, rotation=30, ha='right')
plt.title("Top 10 Streets by Accident Count\n(with Average Weekly Accidents)")
plt.xlabel("Street Name")
plt.ylabel("Total Accident Count")

# Adjust layout to prevent clipping
plt.subplots_adjust(bottom=0.25, top=0.85)

# Annotate bars with average weekly accident count
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
