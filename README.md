# Traffic Violations Insight System

## Project Overview

An interactive traffic violation analytics dashboard built to clean, analyze, and visualize traffic stop records.
The project focuses on identifying common violations, high-risk locations, time-based trends, vehicle patterns, demographic patterns, and accident-related insights using Python, Streamlit, Matplotlib, Pydeck, and MySQL summary analysis.

## Tech Stack

* Python
* Pandas
* Streamlit
* Matplotlib
* Seaborn
* Pydeck
* MySQL
* SQLAlchemy / PyMySQL
* Jupyter Notebook

## Dataset

The project uses a traffic violations dataset containing more than 20 lakh records with information such as stop date, stop time, location, latitude, longitude, violation type, vehicle details, driver demographics, accident indicators, and enforcement-related fields.

## Data Cleaning & Preprocessing

The dataset was cleaned and prepared before analysis. Major cleaning steps include:

* Removed duplicate records
* Standardized date and time columns
* Created a combined `stop_datetime` column
* Converted boolean columns such as Accident, Fatal, Alcohol, HAZMAT, and Commercial Vehicle into True/False values
* Cleaned and validated Latitude and Longitude values
* Replaced invalid coordinates such as 0 values with missing values
* Cleaned invalid location values
* Dropped high-missing search-related columns
* Standardized categorical columns such as Gender, Race, VehicleType, Violation Type, and Make
* Normalized major vehicle make names such as TOYT to TOYOTA, HOND to HONDA, NISS to NISSAN, CHEV/CHEVY to CHEVROLET
* Optimized data types to reduce memory usage

## Feature Engineering

Additional features were created to support analysis and dashboard visualizations:

* `stop_datetime`
* `date`
* `time`
* `hour`
* `month`
* `day`
* `time_bucket`
* `accident_severity`
* `violation_count`

## Exploratory Data Analysis

Structured EDA was performed to answer the following questions:

* What are the most common violations?
* Which areas or coordinates have the highest traffic incidents?
* Do certain demographics correlate with specific violation types?
* How does violation frequency vary by time of day, weekday, or month?
* What types of vehicles are most often involved in violations?
* How often do violations involve accidents, injuries, or vehicle damage?

## Streamlit Dashboard Features

The Streamlit dashboard includes:

* Global sidebar filters
* Search button to apply filters
* Home / Overview page
* Violation Analysis page
* Time Analysis page
* Geographic Analysis page
* Vehicle Analysis page
* Demographic Analysis page

Dashboard features include:

* Violation type distribution
* Time bucket distribution
* Monthly violation trend
* Top violation descriptions
* Top legal charge codes
* Incident hotspot heatmap
* Violation map by type
* Top high-risk locations
* Hourly and weekday violation trends
* Vehicle make, model, color, and type analysis
* Gender and race-based violation analysis
* Accident rate analysis by vehicle make and demographics

## MySQL / SQL Analysis

MySQL was used for SQL-based summary analysis.
Since the cleaned dataset contains more than 20 lakh records, analytical summary tables were created and stored in MySQL for efficient querying.

SQL summary tables include:

* `violation_type_summary`
* `top_locations_summary`
* `monthly_violation_summary`
* `vehicle_make_summary`
* `gender_summary`
* `race_summary`
* `accident_summary`

SQL queries were written to analyze:

* Most common violation types
* Top high-risk locations
* Monthly violation trends
* Most common vehicle makes
* Gender-wise violations
* Race-wise violations
* Accident-related cases

All SQL queries are stored in:

```text
sql/sql_queries.sql
```

## Project Structure

traffic_violations_analysis.ipynb
traffic_violations_dashboard.py

Project Structure:

```text
Traffic_Violations_Project/
│
├── data/
│   ├── raw/
│   │   └── raw_traffic.csv
│   │
│   └── cleaned/
│       └── cleaned_traffic_stops.csv
│
├── sql/
│   └── sql_queries.sql
│
├── create_sql_summaries.py
├── README.md
├── traffic_violations_analysis.ipynb
└── traffic_violations_dashboard.py
```

## How to Run

Install required libraries:

```bash
pip install streamlit pandas matplotlib pydeck sqlalchemy pymysql mysql-connector-python
```

Run the Streamlit dashboard:

```bash
streamlit run traffic_violations_dashboard.py
```

To create MySQL summary tables:

```bash
python create_sql_summaries.py
```

## Key Insights

* Warning and citation records form the majority of violation types.
* Certain road intersections and locations show higher violation density.
* Violations vary by hour, weekday, month, and time bucket.
* Automobiles are the most common vehicle type involved in violations.
* Major vehicle makes such as Toyota, Honda, Ford, Nissan, and Chevrolet appear frequently.
* Driver demographics such as gender and race show different violation distributions.
* Accident-related indicators such as property damage, personal injury, fatality, and alcohol involvement were analyzed separately.

## Conclusion

This project demonstrates the complete data analytics workflow, including data cleaning, preprocessing, feature engineering, structured EDA, interactive dashboard development, and SQL-based summary analysis. The final Streamlit dashboard helps users explore traffic violation trends, hotspots, vehicle patterns, demographic insights, and accident-related information interactively.