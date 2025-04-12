import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Data ---
df = pd.read_csv(r"D:\unishitz\4thsem\int375\EDA-Project\NYC_Collisions\NYC_Collisions.csv")

# Ensure that the numeric columns are read correctly; here, we focus on "Persons Injured"
df['Persons Injured'] = pd.to_numeric(df['Persons Injured'], errors='coerce')
# Optionally, fill NaN values with 0 for our analysis
df['Persons Injured'] = df['Persons Injured'].fillna(0)

# --- Visualize Data Quality: Boxplot Before Outlier Removal ---
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Persons Injured'])
plt.title("Boxplot of Persons Injured (Before Outlier Removal)")
plt.xlabel("Persons Injured")
plt.tight_layout()
plt.savefig("boxplot_before_outliers.png")
plt.show()

# --- Outlier Detection using IQR Method ---
Q1 = df['Persons Injured'].quantile(0.25)
Q3 = df['Persons Injured'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outliers = df[(df['Persons Injured'] < lower_bound) | (df['Persons Injured'] > upper_bound)]
print(f"Number of outliers in 'Persons Injured': {outliers.shape[0]}")
# Remove outliers from the dataset for analysis
df_clean = df[(df['Persons Injured'] >= lower_bound) & (df['Persons Injured'] <= upper_bound)]

# --- Visualize Data Quality: Boxplot After Outlier Removal ---
plt.figure(figsize=(10, 6))
sns.boxplot(x=df_clean['Persons Injured'])
plt.title("Boxplot of Persons Injured (After Outlier Removal)")
plt.xlabel("Persons Injured")
plt.tight_layout()
plt.savefig("boxplot_after_outliers.png")
plt.show()

# --- Data Quality Summary ---
print("Summary statistics before outlier removal:")
print(df['Persons Injured'].describe())
print("\nSummary statistics after outlier removal:")
print(df_clean['Persons Injured'].describe())
