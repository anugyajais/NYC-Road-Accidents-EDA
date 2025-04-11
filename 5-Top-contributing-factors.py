import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")
df['Contributing Factor'] = df['Contributing Factor'].fillna('Unknown')

# --- Contributing Factor Assessment ---
cf_counts = df['Contributing Factor'].value_counts()
unspecified_count = cf_counts.get("Unspecified", 0)
cf_counts_filtered = cf_counts.drop("Unspecified", errors='ignore')
specified_count = cf_counts_filtered.sum()

# --- Visualization ---
plt.figure(figsize=(10, 7))

top_factors = cf_counts_filtered.head(10)
ax = sns.barplot(
    x=top_factors.values,
    y=top_factors.index,
    palette="viridis",
    hue=None,
    legend=False
)

plt.title("Top 10 Contributing Factors for Accidents", fontsize=15)
plt.xlabel("Number of Accidents", fontsize=13)
plt.ylabel("Contributing Factor", fontsize=13)

# Extend x-axis to give room for data labels
max_val = max(top_factors.values)
plt.xlim(0, max_val * 1.1)

# Annotate bars with their values
for p in ax.patches:
    width = p.get_width()
    ax.text(width + max_val * 0.01,
            p.get_y() + p.get_height() / 2,
            f"{int(width)}",
            ha='left', va='center', fontsize=11, color='black')

# Add note about unspecified vs specified, raised slightly
plt.figtext(0.5, 0.01,
            f"Total accidents with 'Unspecified': {unspecified_count} | Total with specified factors: {specified_count}",
            wrap=True, horizontalalignment='center', fontsize=12, color='gray')

# Adjust plot to leave space at the bottom for text
plt.tight_layout(rect=[0, 0.03, 1, 1])  # [left, bottom, right, top]
plt.savefig("top_contributing_factors_with_weekly_avg.png")
plt.show()
