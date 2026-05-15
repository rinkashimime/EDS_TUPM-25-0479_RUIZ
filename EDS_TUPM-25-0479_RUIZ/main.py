# %%
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import skew
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
raw_file_path = os.path.join(script_dir, 'HVAC_NE_EC_19-21.csv')
data_dir = os.path.join(script_dir, 'data')
outputs_dir = os.path.join(script_dir, 'outputs')

# Create mandatory project folders for GitHub/Pipeline compliance
for folder in [data_dir, outputs_dir]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created directory: {folder}")

# %%
# Load the verified dataset

df = None
try:
    df = pd.read_csv(raw_file_path)
    # Save the original to the data folder per architecture requirements
    df.to_csv(os.path.join(data_dir, 'dataset_original.csv'), index=False)
    print(f"[SUCCESS] AHU Telemetry Ingested: {len(df)} rows found.")
    print(df.head())  # Shows the first 5 rows in your notebook-like output
except Exception as e:
    print(f"[ERROR] Ingestion failed: {e}")
    sys.exit(1)

# %%
# Data Cleaning
cleaned_df = df.dropna().drop_duplicates()

# UNIQUE FILTER LOGIC: Isolating high-load periods (> 5.0 kW)
# In Duct Leakage analysis, high-load cycles reveal pressure-drop anomalies.
if 'Power' in cleaned_df.columns:
    cleaned_df = cleaned_df[cleaned_df['Power'] > 5.0]

# Save cleaned data to the mandatory data folder
cleaned_df.to_csv(os.path.join(data_dir, 'dataset_cleaned.csv'), index=False)
print(f"[SUCCESS] Unique Filter applied. Sample size: {len(cleaned_df)} rows.")

# %%
# Convert to NumPy for high-performance engineering calculations
power_vals = cleaned_df['Power'].to_numpy()

findings = {
    "Mean_Load (kW)": np.mean(power_vals),
    "Load_Variance": np.var(power_vals),
    "Load_Skewness": skew(power_vals),
    "Peak_Observation": np.max(power_vals)
}

print("--- ENGINEERING METRICS FOR HVA-04 ---")
for key, value in findings.items():
    print(f"{key}: {value:.4f}")

# %%
# 1. Static Scatter Plot: Pressure vs. Power (The "Leakage Signature")
fig_static = px.scatter(cleaned_df, x='SP_Return', y='Power', 
                         title="HVA-04: Duct Pressure vs. Power Correlation")
fig_static.write_image(os.path.join(outputs_dir, 'static_scatter.png'))

# 2. Animated Behavior over Time
# We use a slice (first 500 rows) to keep the animation smooth in the browser
fig_anim = px.scatter(cleaned_df.head(500), x='SP_Return', y='Power',
                      animation_frame='Timestamp', 
                      title="Dynamic Pressure-Power Fluctuations")
fig_anim.write_html(os.path.join(outputs_dir, 'animated_leakage.html'))

print("[SUCCESS] Static PNG and Animated HTML saved to /outputs folder.")
fig_static.show() # Display the plot directly in your notebook

# %% [markdown]
# 


