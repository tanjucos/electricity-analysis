import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title & short intro
st.title("Global Electricity Production Data")
st.markdown(
    """This page shows a simple trend of **global electricity production over time**.
    Data is loaded directly from the repository, cleaned by dropping missing values,
    and aggregated by year before plotting."""
)

# Data source note
st.caption(
    "Data source: GitHub • "
    "[electricity-analysis / data/raw/global_electricity_production_data.csv]"
    "(https://www.kaggle.com/datasets/sazidthe1/global-electricity-production)"
)


# Step 1: Load the dataset
url = "https://raw.githubusercontent.com/tanjucos/electricity-analysis/main/data/raw/global_electricity_production_data.csv"
df = pd.read_csv(url)

# Step 2: Drop missing 'value' rows
df_clean = df.dropna(subset=['value']).copy()

# Step 3: Convert 'date' column to datetime
df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')

# Step 4: Drop rows where date conversion failed
df_clean = df_clean[df_clean['date'].notnull()].copy()

# Step 5: Extract 'year' as integer
df_clean['year'] = df_clean['date'].dt.year.astype(int)

# Quick stats text (no tables)
years_min = int(df_clean['year'].min())
years_max = int(df_clean['year'].max())
rows_used = len(df_clean)

st.markdown(
    f"- **Years covered:** {years_min}–{years_max}  \n"
    f"- **Rows used after cleaning:** {rows_used}  \n"
    f"- **Unit:** values reported in the `unit` column (typically GWh)."
)


# ---- Plot only the chart ----
yearly_production = df_clean.groupby('year')['value'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(yearly_production['year'], yearly_production['value'], marker='o')
ax.set_title('Global Electricity Production Over Time')
ax.set_xlabel('Year')
ax.set_ylabel('Total Electricity Production (GWh)')
ax.grid(True)

st.pyplot(fig)

# Methods / notes
with st.expander("What happens under the hood?"):
    st.markdown(
        "- Drop rows with missing `value`.\n"
        "- Parse `date` to datetime; drop rows where parsing fails.\n"
        "- Create a `year` column from `date`.\n"
        "- Group by `year` and sum `value` to plot the trend."
    )