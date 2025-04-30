import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load SQLite database
db_path = "Cattery_Registration.sqlite"  # Replace with your actual path
conn = sqlite3.connect(db_path)

# Query the database
query = """
SELECT 
    W.ZLITTER AS id,
    W.ZWEIGHT AS weight,
    W.ZTIME AS weight_time,
    L.ZSEX AS sex,
    L.ZCOLOR AS hair_color,
    L.ZHAIR AS hair_type,
    FirstWeights.first_weight AS birth_weight,
    P.ZDELIVERY AS plan_delivery
FROM ZWEIGHTS W
JOIN ZLITTERS L ON W.ZLITTER = L.Z_PK
JOIN ZPLANS P ON L.ZPLAN = P.Z_PK
LEFT JOIN (
    SELECT ZLITTER, ZWEIGHT AS first_weight
    FROM ZWEIGHTS
    WHERE Z_PK IN (
        SELECT Z_PK FROM (
            SELECT Z_PK, ZLITTER,
                   ROW_NUMBER() OVER (PARTITION BY ZLITTER ORDER BY ZTIME ASC) AS rn
            FROM ZWEIGHTS
        )
        WHERE rn = 1
    )
) AS FirstWeights ON W.ZLITTER = FirstWeights.ZLITTER
"""

df = pd.read_sql_query(query, conn)

# Convert dates from timestamps or strings if needed
df['weight_time'] = pd.to_datetime(df['weight_time'] + 978307200, unit='s')
df['plan_delivery'] = pd.to_datetime(df['plan_delivery'] + 978307200, unit='s')

df['normalized_birth_weight'] = df['birth_weight'] / df['birth_weight'].max() / 10
# Compute "days since delivery"
df['age_in_days'] = ((df['weight_time'] - df['plan_delivery']) / pd.Timedelta(days=1)).astype(float)
df = df[df['age_in_days'] <= 60]

# Add month of birth from delivery
df['month_of_birth'] = df['plan_delivery'].dt.month_name()

# Prepare first weights data (for boxplot, sorted by time)
first_weights_df = (
    df.sort_values('weight_time')
      .drop_duplicates(['id'])  # Assuming first weight per litter
      .copy()
)

df.to_csv("result.csv", index=False)

# Rename columns for better readability in df
df = df.rename(columns={
    "age_in_days": "Age (Days)",
    "weight": "Weight (g)",
    "month_of_birth": "Month of Birth",
    "normalized_birth_weight": "Normalized Birth Weight",
    "hair_color": "Coat Color",
    "hair_type": "Hair Type",
    "birth_weight": "Birth Weight (g)",
    "sex": "Sex"
})

# Rename columns for better readability in first_weights_df
first_weights_df = first_weights_df.rename(columns={
    "birth_weight": "Birth Weight (g)",
    "sex": "Sex",
    "month_of_birth": "Month of Birth",
    "hair_color": "Coat Color",
    "hair_type": "Hair Type"
})

print(df['weight_time'].min())
print(df.count())

# --- Plot 1: Growth Curve ---
fig_growth = px.scatter(
    df,
    x="Age (Days)",
    y="Weight (g)",
    color="Birth Weight (g)",
    size="Normalized Birth Weight",
    hover_data=["Coat Color", "Hair Type", "Birth Weight (g)", "Sex", "Month of Birth"],
    title="Weight vs Days Since Born",
    color_continuous_scale=px.colors.sequential.Pinkyl,
    trendline="ols",
    template="simple_white"
)
fig_growth.update_layout(
    xaxis_title="Days Since Birth",
    yaxis_title="Weight (g)"
)
fig_growth.write_html("growth-curve.html")


# --- Plot 2: Boxplot of Born Weights ---
fig_box = px.box(
    first_weights_df,
    x="Birth Weight (g)",
    y="Sex",
    color="Sex",
    hover_data=["Coat Color", "Hair Type", "Sex", "Month of Birth"],
    title="Distribution of Litter Born Weights",
    orientation="h",
    template="simple_white"
)
fig_box.update_layout(
    xaxis_title="Birth Weight (g)",
    yaxis_title="",
    boxmode="group"
)
fig_box.write_html("born-weights-distribution.html")


print("Plots saved: growth_curve.html, born_weights_distribution.html")
