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
    M.ZBEFORE AS before,
    M.ZAFTER AS after,
    M.ZSTART AS start,
    M.ZEND AS end,
    S.ZCONSUMABLE AS consumable,
    S.ZNAME AS name,
    COUNT(DISTINCT A.Z_PK) AS participants
FROM ZMEASURES M
JOIN ZSUBJECTS S ON M.ZSUBJECT = S.Z_PK
LEFT JOIN Z_1MEASURE MA ON MA.Z_3MEASURE = M.Z_PK
LEFT JOIN ZADULTS A ON A.Z_PK = MA.Z_1ADULT
WHERE M.ZEND IS NOT NULL
GROUP BY M.Z_PK;
"""

df = pd.read_sql_query(query, conn)

# Convert dates from timestamps or strings if needed
df['start'] = pd.to_datetime(df['start'] + 978307200, unit='s')
df['end'] = pd.to_datetime(df['end'] + 978307200, unit='s')

df['total_usage'] = (df['before'] - df['after']) * (df['consumable'] * 2 - 1)

df['duration_in_days'] = (((df['end'] - df['start']) / pd.Timedelta(days=1)).astype(float)).clip(lower=1.0)

df['usage_per_day'] = df['total_usage'] / df['duration_in_days'] / df['participants']

df.to_csv("consumption.csv", index=False)

print(df['start'].min())
print(df.count())

# --- Plot: Boxplot of Born Weights ---
fig_box = px.box(
    df,
    x="usage_per_day",
    y="name",
    color="name",
    hover_data=[],
    title="Distribution of Consumptions",
    orientation="h",
    labels={
        "usage_per_day": "Usage (g / day)",
        "name": "Type"
    },
    template="simple_white"
)
fig_box.update_traces(boxpoints=False)
fig_box.update_layout(
    xaxis_title="Usage (g / day)",
    yaxis_title="Type of Usage",
    boxmode="group"
)
fig_box.write_html("consumption-distribution.html")


print("Plots saved: consumption-distribution.html")
