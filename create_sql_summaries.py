import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus


# MySQL connection details
user = "root"
password = quote_plus("Admin@123")
host = "localhost"
database = "traffic_violations_db"


# Create connection engine
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)


# Load cleaned dataset
df = pd.read_csv("data/cleaned/cleaned_traffic_stops.csv")


# Convert date column for time-based summaries
df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")


# 1. Violation type summary
violation_type_summary = (
    df["Violation Type"]
    .value_counts()
    .reset_index()
)

violation_type_summary.columns = ["violation_type", "total_violations"]


# 2. Top locations summary
top_locations_summary = (
    df["Location"]
    .value_counts()
    .head(50)
    .reset_index()
)

top_locations_summary.columns = ["location", "total_violations"]


# 3. Monthly violation summary
monthly_violation_summary = (
    df
    .dropna(subset=["date"])
    .groupby(df["date"].dt.to_period("M"))
    .size()
    .reset_index(name="total_violations")
)

monthly_violation_summary["date"] = monthly_violation_summary["date"].astype(str)
monthly_violation_summary.columns = ["month", "total_violations"]


# 4. Vehicle make summary
vehicle_make_summary = (
    df["Make"]
    .value_counts()
    .head(50)
    .reset_index()
)

vehicle_make_summary.columns = ["vehicle_make", "total_violations"]


# 5. Gender summary
gender_summary = (
    df["Gender"]
    .value_counts()
    .reset_index()
)

gender_summary.columns = ["gender", "total_violations"]


# 6. Race summary
race_summary = (
    df["Race"]
    .value_counts()
    .reset_index()
)

race_summary.columns = ["race", "total_violations"]


# 7. Accident summary
accident_summary = pd.DataFrame({
    "metric": [
        "Accident",
        "Personal Injury",
        "Property Damage",
        "Fatal",
        "Alcohol"
    ],
    "total_cases": [
        int(df["Accident"].sum()),
        int(df["Personal Injury"].sum()),
        int(df["Property Damage"].sum()),
        int(df["Fatal"].sum()),
        int(df["Alcohol"].sum())
    ]
})


# Upload summary tables to MySQL
violation_type_summary.to_sql(
    "violation_type_summary",
    con=engine,
    if_exists="replace",
    index=False
)

top_locations_summary.to_sql(
    "top_locations_summary",
    con=engine,
    if_exists="replace",
    index=False
)

monthly_violation_summary.to_sql(
    "monthly_violation_summary",
    con=engine,
    if_exists="replace",
    index=False
)

vehicle_make_summary.to_sql(
    "vehicle_make_summary",
    con=engine,
    if_exists="replace",
    index=False
)

gender_summary.to_sql(
    "gender_summary",
    con=engine,
    if_exists="replace",
    index=False
)

race_summary.to_sql(
    "race_summary",
    con=engine,
    if_exists="replace",
    index=False
)

accident_summary.to_sql(
    "accident_summary",
    con=engine,
    if_exists="replace",
    index=False
)


print("SQL summary tables created successfully.")