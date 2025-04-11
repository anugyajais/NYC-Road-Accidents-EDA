import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file (update the path as needed)
df = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")


# --- Accident Hotspot Identification ---

# Clean location columns: fill missing values with 'Unknown'
df['Borough'] = df['Borough'].fillna('Unknown')
df['Street Name'] = df['Street Name'].fillna('Unknown')

# grouping by Borough and Street Name, counting accidents
hotspots = df.groupby(['Borough', 'Street Name']).size().reset_index(name='Accident_Count')

# sorting by accident count in descending order and select the top 20 hotspots
top_hotspots = hotspots.sort_values('Accident_Count', ascending=False).head(20)


# Create a horizontal bar plot to display top accident hotspots
plt.figure(figsize=(12, 8))
sns.barplot(data=top_hotspots, y='Street Name', x='Accident_Count', hue='Borough', dodge=False)
plt.title("Top 20 Accident Hotspots by Street and Borough")
plt.xlabel("Number of Accidents")
plt.ylabel("Street Name")
plt.tight_layout()
plt.savefig("accident_hotspots.png")
plt.show()


