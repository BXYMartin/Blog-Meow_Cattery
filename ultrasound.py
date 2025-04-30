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
    S.ZHD as hd,
    S.ZTIME as time,
    S.ZCOUNT as count,
    P.ZCONCEPTION as conception,
    P.ZDELIVERY as delivery,
    P.Z_PK as id
FROM ZSCANS S
JOIN ZPLANS P ON S.ZPLAN = P.Z_PK
WHERE S.ZHD IS NOT NULL
"""

df = pd.read_sql_query(query, conn)

# Convert dates from timestamps or strings if needed
df['time'] = pd.to_datetime(df['time'] + 978307200, unit='s')
df['conception'] = pd.to_datetime(df['conception'] + 978307200, unit='s')
df['delivery'] = pd.to_datetime(df['delivery'] + 978307200, unit='s')

# Compute "days since delivery"
df['days_after_conception'] = ((df['time'] - df['conception']) / pd.Timedelta(days=1)).astype(float)
df['days_before_delivery'] = ((df['delivery'] - df['time']) / pd.Timedelta(days=1)).astype(float)

df.to_csv("ultrasound.csv", index=False)

print(df['time'].min())
print(df.count())

# --- Plot 1: Growth Curve ---
fig_growth = px.scatter(
    df,
    x="days_before_delivery",
    y="hd",
    color="id",
    size="count",
    hover_data=["count", "days_before_delivery", "days_after_conception"],
    title="Head Diameters from Ultrasound Scans vs Days Before Delivery",
    color_discrete_map=px.colors.cyclical,
    trendline="ols",
    labels={
        "hd": "Head Diameter (cm)",
        "days_before_delivery": "Days Before Delivery",
        "days_after_conception": "Days After First Mate",
        "count": "Count"
    },
    template="simple_white"
)
fig_growth.update_coloraxes(showscale=False)
fig_growth.update_layout(
    xaxis_title="Days Before Delivery",
    yaxis_title="Head Diameter (cm)"
)
fig_growth.write_html("ultrasound-growth-before-delivery.html")


# --- Plot 2: Growth Curve ---
fig_growth = px.scatter(
    df,
    x="days_after_conception",
    y="hd",
    color="id",
    size="count",
    hover_data=["count", "days_before_delivery", "days_after_conception"],
    title="Head Diameters from Ultrasound Scans vs Days After First Mate",
    color_discrete_map=px.colors.cyclical,
    trendline="ols",
    labels={
        "hd": "Head Diameter (cm)",
        "days_before_delivery": "Days Before Delivery",
        "days_after_conception": "Days After First Mate",
        "count": "Count"
    },
    template="simple_white"
)
fig_growth.update_coloraxes(showscale=False)
fig_growth.update_layout(
    xaxis_title="Days After First Mate",
    yaxis_title="Head Diameter (cm)"
)
fig_growth.write_html("ultrasound-growth-after-mate.html")


print("Plots saved")
