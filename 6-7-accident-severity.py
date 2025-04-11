import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load & Clean Data ---
df = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")

# Fill missing values for 'Contributing Factor'
df['Contributing Factor'] = df['Contributing Factor'].fillna('Unknown')

# Ensure numeric columns are numeric; convert and fill NaN with 0
numeric_cols = ['Persons Killed', 'Pedestrians Killed', 'Cyclists Killed', 'Motorists Killed',
                'Pedestrians Injured', 'Cyclists Injured', 'Motorists Injured']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# --- Objective 6: Fatal Accident Causality Analysis ---
# Create a 'Total Fatalities' column by summing fatalities across categories
df['Total Fatalities'] = (df['Persons Killed'] + 
                          df['Pedestrians Killed'] + 
                          df['Cyclists Killed'] + 
                          df['Motorists Killed'])

# Filter fatal accidents (where Total Fatalities > 0)
fatal_df = df[df['Total Fatalities'] > 0]

# Group by 'Contributing Factor' and count fatal accidents
fatal_cf_counts = fatal_df['Contributing Factor'].value_counts()

# Plot the top contributing factors in fatal accidents
plt.figure(figsize=(10, 6))
ax1 = sns.barplot(x=fatal_cf_counts.head(10).values, 
                  y=fatal_cf_counts.head(10).index, 
                  palette="magma", 
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
# Calculate total injuries and fatalities for pedestrians, cyclists, and motorists
ped_injured = df['Pedestrians Injured'].sum()
ped_killed  = df['Pedestrians Killed'].sum()
cycl_injured = df['Cyclists Injured'].sum()
cycl_killed  = df['Cyclists Killed'].sum()
motor_injured = df['Motorists Injured'].sum()
motor_killed  = df['Motorists Killed'].sum()

# Create a summary DataFrame
injury_data = {
    "Category": ["Pedestrians", "Cyclists", "Motorists"],
    "Injured": [ped_injured, cycl_injured, motor_injured],
    "Killed": [ped_killed, cycl_killed, motor_killed]
}
injury_df = pd.DataFrame(injury_data)

# --- Visualization: Stacked Bar Chart for Injury Severity Profiling ---
plt.figure(figsize=(8, 6))
categories = injury_df["Category"]
injured = injury_df["Injured"]
killed = injury_df["Killed"]
width = 0.6

# Plot the injured counts
bars_injured = plt.bar(categories, injured, width=width, label="Injured", color="skyblue")
# Plot the killed counts on top of injured counts
bars_killed = plt.bar(categories, killed, width=width, bottom=injured, label="Killed", color="salmon")

plt.title("Injury Severity Profiling", fontsize=15)
plt.xlabel("Category", fontsize=13)
plt.ylabel("Total Count", fontsize=13)
plt.legend()

# Annotate the "Injured" segment
for bar in bars_injured:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height / 2,
             f"{int(height)}", ha="center", va="center", fontsize=11, color="black")

# Annotate the "Killed" segment (on top of the injured segment)
for bar, base in zip(bars_killed, injured):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, base + height / 2,
             f"{int(height)}", ha="center", va="center", fontsize=11, color="black")

plt.tight_layout()
plt.savefig("injury_severity_stacked.png")
plt.show()
