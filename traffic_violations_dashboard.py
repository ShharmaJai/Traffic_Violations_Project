import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Page configuration
st.set_page_config(
    layout="wide"
)


# Load cleaned dataset
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned/cleaned_traffic_stops.csv")
    df["date"] = pd.to_datetime(
    df["date"],
    format="%d/%m/%Y",
    errors="coerce"
)
    return df

df = load_data()


# Create a separate dataframe for dashboard filters
filtered_df = df.copy()




# Sidebar
st.sidebar.title('🚦 Traffic Violations Insight System')
st.sidebar.divider()
st.sidebar.header("🔍 Global Filters")

with st.sidebar.form("filter_form"):

    # Gender
    gender_options = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    selected_gender = st.selectbox("Select Gender", gender_options)

    if selected_gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == selected_gender]


    # Race
    race_options = ["All"] + sorted(df["Race"].dropna().unique().tolist())
    selected_race = st.selectbox("Select Race", race_options)

    if selected_race != "All":
        filtered_df = filtered_df[filtered_df["Race"] == selected_race]


    # Vehicle Type
    vehicle_options = ["All"] + sorted(df["VehicleType"].dropna().unique().tolist())
    selected_vehicle = st.selectbox("Select Vehicle Type", vehicle_options)

    if selected_vehicle != "All":
        filtered_df = filtered_df[filtered_df["VehicleType"] == selected_vehicle]


    # Violation Type
    violation_options = ["All"] + sorted(df["Violation Type"].dropna().unique().tolist())
    selected_violation = st.selectbox("Select Violation Type", violation_options)

    if selected_violation != "All":
        filtered_df = filtered_df[filtered_df["Violation Type"] == selected_violation]


    # Location
    location_options = ["All"] + sorted(df["Location"].dropna().unique().tolist())
    selected_location = st.selectbox("Select Location", location_options)

    if selected_location != "All":
        filtered_df = filtered_df[filtered_df["Location"] == selected_location]


    # Date
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    selected_date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )

    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range

        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date) &
            (filtered_df["date"].dt.date <= end_date)
        ]

    search_button = st.form_submit_button("Search")

st.sidebar.divider()
st.sidebar.header('Navigate to page')
selected_page = st.sidebar.selectbox(
    "Select Page",
    [
        "🏠 Home / Overview",
        "🗺️ Geographic Analysis",
        "📋 Violation Analysis",
        "⏰ Time Analysis",
        "🚘 Vehicle Analysis",
        "👥 Demographic Analysis"   
    ]
)

# Dashboard title
if selected_page == "🏠 Home / Overview":

    st.title("🚦 Traffic Violations Insight System")
    st.write("Interactive dashboard for analyzing cleaned traffic violation records.")

    st.subheader("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", filtered_df.shape[0])

    with col2:
        st.metric("Total Columns", filtered_df.shape[1])

    with col3:
        st.metric("Accident Cases", int(filtered_df["Accident"].sum()))

    with col4:
        st.metric("Fatal Cases", int(filtered_df["Fatal"].sum()))

    st.subheader("Sample Data")
    st.dataframe(filtered_df.head(21))




    # Overview Charts
    st.subheader("Overview Insights")

    chart_col1, chart_col2 = st.columns(2)


    # Chart 1: Violation Type Distribution
    with chart_col1:
        st.markdown('### 📊 Violation Type Distribution')
        violation_counts = filtered_df['Violation Type'].value_counts()

        fig, ax = plt.subplots(figsize = (7,4))

        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')

        ax.barh(violation_counts.index, violation_counts.values, color = '#4C78A8')

        ax.set_xlabel('Number of Violations', color = 'white')
        ax.set_ylabel('Violation Type', color = 'white')

        ax.tick_params(axis = 'x', colors = 'white')
        ax.tick_params(axis = 'y', colors = 'white')

        lower_limit = 0
        upper_limit = 1200000
        ax.set_xlim(lower_limit, upper_limit)

        def format_thousands(x, pos):
            return f'{int(x/1000)}k'
        
        ax.xaxis.set_major_formatter(FuncFormatter(format_thousands))

        ax.invert_yaxis()
        ax.margins(y = 0)

        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.subplots_adjust(left=0.18, right=0.95, top=0.82, bottom=0.18)

        st.pyplot(fig, use_container_width=True)
        


    # Chart 2: Violations by Time of Day
    with chart_col2:
        st.markdown("### 🕒 Violations by Time of Day")

        time_counts = filtered_df["time_bucket"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        wedges, texts, autotexts = ax.pie(
            time_counts.values,
            labels=None,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.75,
            radius=0.90,
            center=(0, 0.11),
            wedgeprops={"width": 0.35},
            textprops={"color": "white", "fontsize": 9}
        )

        legend = ax.legend(
            wedges,
            time_counts.index,
            title="Time Bucket",
            loc="center left",
            bbox_to_anchor=(0.95, 0.5),
            frameon=False,
            labelcolor="white"
        )
        
        legend.get_title().set_color("#ECF0F5")
        
        ax.set_aspect("equal")

        ax.set_xlim(-1.15, 1.75)
        ax.set_ylim(-1.00, 1.00)

        fig.subplots_adjust(left=0.05, right=0.85, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)
        
        
    st.divider()



   # Monthly Violation Trend
    st.markdown("### 📈 Monthly Violation Trend")

    monthly_df = filtered_df.dropna(subset=['date'])
    monthly_trend = (filtered_df.groupby(filtered_df['date'].dt.to_period('M')).size())

    monthly_trend.index = monthly_trend.index.to_timestamp()

    fig, ax = plt.subplots(figsize=(14, 5))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    ax.plot(
        monthly_trend.index,
        monthly_trend.values,
        color="#6C63FF",
        linewidth=2
    )

    ax.fill_between(
        monthly_trend.index,
        monthly_trend.values,
        color = '#6C63FF',
        alpha = 0.3
    )
    ax.set_xlabel("Year", color="white")
    ax.set_ylabel("Violations", color="white")

    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")

    def format_thousands(x, pos):
        return f"{int(x/1000)}k"

    ax.yaxis.set_major_formatter(FuncFormatter(format_thousands))

    # Show x-axis labels year-wise
    years = monthly_trend.index.year.unique()

    year_positions = [
        monthly_trend[monthly_trend.index.year == year].index[0]
        for year in years
    ]

    ax.set_xticks(year_positions)
    ax.set_xticklabels(years, rotation=0, color="white")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(axis="y", alpha=0.2)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)




# Geographical Incident Hotspots
if selected_page == "🗺️ Geographic Analysis":
    st.title("🗺️Geographic Analysis")
    st.subheader("Incident Hotspot Heatmap")

    map_df = filtered_df[["Latitude", "Longitude"]].dropna()

    map_df = map_df.rename(columns={
        "Latitude": "latitude",
        "Longitude": "longitude"
    })

    if not map_df.empty:
        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=map_df,
            get_position=["longitude", "latitude"],
            radius_pixels=60
        )

        view_state = pdk.ViewState(
            latitude=map_df["latitude"].mean(),
            longitude=map_df["longitude"].mean(),
            zoom=9,
            pitch=0
        )

        heatmap = pdk.Deck(
            layers=[heatmap_layer],
            initial_view_state=view_state
        )

        st.pydeck_chart(heatmap)

    else:
        st.warning("No valid latitude and longitude data available for the selected filters.")

    st.divider()

    # Violation Map by Type + Top Locations
    st.subheader("Violation Map by Type and Top Locations")

    col1, col2 = st.columns([2, 1])


    # Left Side: Violation Map by Type
    with col1:
        st.markdown("### 🔴 Violation Map by Type")

        category_map_df = filtered_df[
            ["Latitude", "Longitude", "Violation Type"]
        ].dropna()

        category_map_df = category_map_df.rename(columns={
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Violation Type": "violation_type"
        })

        # Use sample for better performance if data is very large
        if len(category_map_df) > 50000:
            category_map_df = category_map_df.sample(50000, random_state=42)

        def assign_color(violation_type):
            if violation_type == "WARNING":
                return [255, 0, 0, 160]
            elif violation_type == "CITATION":
                return [0, 0, 225, 160]
            elif violation_type == "ESERO":
                return [0, 255, 0, 160]
            else:
                return [255, 255, 255, 120]

        category_map_df["color"] = category_map_df["violation_type"].apply(assign_color)

        if not category_map_df.empty:
            category_layer = pdk.Layer(
                'ScatterplotLayer',
                data = category_map_df,
                get_position = ['longitude', 'latitude'],
                get_fill_color = 'color',
                get_radius = 60, 
                pickable = True
            )

            category_view_state = pdk.ViewState(
                latitude = category_map_df['latitude'].mean(),
                longitude = category_map_df['longitude'].mean(),
                zoom = 9,
                pitch = 0
            )

            category_map = pdk.Deck(
                layers = [category_layer],
                initial_view_state = category_view_state,
                tooltip = {'text' : 'Violation Type: {violation_type}'}
            )

            st.pydeck_chart(category_map)

            st.caption("Color guide: WARNING 🔴, CITATION 🔵, ESERO 🟢")

        else:
            st.warning("No valid data available for violation type map.")


    # Right Side: Top Locations Table
    with col2:
        st.markdown("### 🏙️ Top Locations")

        top_locations = (
            filtered_df["Location"]
            .value_counts()
            .head(21)
            .reset_index()
        )

        top_locations.columns = ["Location", "Count"]

        st.dataframe(
            top_locations,
            hide_index=True,
            use_container_width=True
        )

# Violation Analysis
if selected_page == "📋 Violation Analysis":

    st.title('📋 Violation Analysis')
    st.write('This section shows the most common violation reasons and violation types.')

    top_descriptions = filtered_df['Description'].value_counts().head(10)

    fig, ax = plt.subplots(figsize = (12, 6))

    fig.patch.set_facecolor("#0E1117")
    fig.patch.set_edgecolor("black")
    fig.patch.set_linewidth(1)

    ax.set_facecolor("#0E1117")

    ax.barh(
        top_descriptions.index,
        top_descriptions.values,
        color = "#4C78A8"
    )

    ax.set_xlabel('Number of Violations', color = "#F2F4F8")
    ax.set_ylabel('Violation Description', color = "#F2F4F8")

    ax.tick_params(axis = 'x', colors = '#F2F4F8')
    ax.tick_params(axis = 'y', colors = '#F2F4F8')

    def format_numbers(x, pos):
        return f'{int(x/1000)}k'
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_numbers))

    ax.invert_yaxis()

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)
    st.divider()


    # Charge Analysis + Violation Type Breakdown
    st.subheader("Charge and Violation Type Analysis")

    violation_col1, violation_col2 = st.columns(2)

    # Chart 1: Violation Type Distribution
    with violation_col1:
        st.markdown('### 📊 Top Violation Charges')
        top_charges = filtered_df["Charge"].value_counts().head(10)

        fig, ax = plt.subplots(figsize = (7,4))

        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')

        ax.barh(top_charges.index, top_charges.values, color = '#4C78A8')

        ax.set_xlabel('Number of Violations', color = 'white')
        ax.set_ylabel('Violation Charge', color = 'white')

        ax.tick_params(axis = 'x', colors = 'white')
        ax.tick_params(axis = 'y', colors = 'white')

        def format_thousands(x, pos):
            return f'{int(x/1000)}k'
        
        ax.xaxis.set_major_formatter(FuncFormatter(format_thousands))

        ax.invert_yaxis()
        ax.margins(y = 0)

        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.subplots_adjust(left=0.18, right=0.95, top=0.82, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    # Chart 2: Violations by Time of Day
    with violation_col2:
        st.markdown("### 🕒 Violations Type Breakdown")

        violation_type_counts = filtered_df["Violation Type"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        wedges, texts, autotexts = ax.pie(
            violation_type_counts.values,
            labels=None,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.75,
            radius=0.90,
            center=(0, 0.11),
            wedgeprops={"width": 0.35},
            textprops={"color": "white", "fontsize": 9}
        )

        legend = ax.legend(
            wedges,
            violation_type_counts.index,
            title="Violation Type",
            loc="center left",
            bbox_to_anchor=(0.95, 0.5),
            frameon=False,
            labelcolor="white"
        )
        
        legend.get_title().set_color("#ECF0F5")
        
        ax.set_aspect("equal")

        ax.set_xlim(-1.15, 1.75)
        ax.set_ylim(-1.00, 1.00)

        fig.subplots_adjust(left=0.05, right=0.85, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


# Time Analysis
if selected_page == "⏰ Time Analysis":

    st.title("⏰ Time-Based Analysis")
    st.write("This section shows how traffic violations vary by hour, weekday, and time bucket.")

    time_col1, time_col2 = st.columns(2)

    # Chart 1: Violations by Hour of Day
    with time_col1:
        st.markdown("### Violations by Hour of Day")

        hourly_counts = filtered_df["hour"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.plot(
            hourly_counts.index,
            hourly_counts.values,
            color="#29B6F6",
            marker="o",
            linewidth=2
        )

        ax.fill_between(
            hourly_counts.index,
            hourly_counts.values,
            color="#29B6F6",
            alpha=0.3
        )

        ax.set_xlabel("Hour", color="#F2F4F8")
        ax.set_ylabel("Count", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8")
        ax.tick_params(axis="y", colors="#F2F4F8")

        def format_thousands(x, pos):
            return f"{int(x / 1000)}k"

        ax.yaxis.set_major_formatter(FuncFormatter(format_thousands))

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(axis="y", alpha=0.2)

        fig.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    # Chart 2: Violations by Day of Week
    with time_col2:
        st.markdown("### Violations by Day of Week")

        weekday_order = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        ]

        weekday_counts = filtered_df["date"].dt.day_name().value_counts()
        weekday_counts = weekday_counts.reindex(weekday_order)

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.bar(
            weekday_counts.index,
            weekday_counts.values,
            color="#9B59B6"
        )

        ax.set_xlabel("Weekday", color="#F2F4F8")
        ax.set_ylabel("Count", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8", rotation=35)
        ax.tick_params(axis="y", colors="#F2F4F8")

        ax.yaxis.set_major_formatter(FuncFormatter(format_thousands))

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(axis="y", alpha=0.2)

        fig.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.25)

        st.pyplot(fig, use_container_width=True)


    st.divider()


    # Chart 3: Time Bucket Distribution
    st.markdown("### 🕒 Time Bucket Distribution")

    time_bucket_counts = filtered_df["time_bucket"].value_counts()

    fig, ax = plt.subplots(figsize=(12, 4))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    ax.barh(
        time_bucket_counts.index,
        time_bucket_counts.values,
        color="#61063E"
    )

    ax.set_xlabel("Number of Violations", color="#F2F4F8")
    ax.set_ylabel("Time Bucket", color="#F2F4F8")

    ax.tick_params(axis="x", colors="#F2F4F8")
    ax.tick_params(axis="y", colors="#F2F4F8")

    ax.xaxis.set_major_formatter(FuncFormatter(format_thousands))

    ax.invert_yaxis()

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)


    st.divider()


    # Chart 4: Weekday x Hour Violation Heatmap
    st.markdown("### 🔥 Weekday × Hour Violation Heatmap")

    heatmap_data = filtered_df.copy()
    heatmap_data["weekday"] = heatmap_data["date"].dt.day_name()

    heatmap_table = pd.crosstab(
        heatmap_data["weekday"],
        heatmap_data["hour"]
    )

    heatmap_table = heatmap_table.reindex(weekday_order)

    fig, ax = plt.subplots(figsize=(14, 5))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    heatmap = ax.imshow(
        heatmap_table,
        aspect="auto",
        cmap="YlOrRd"
    )

    ax.set_xlabel("Hour of Day", color="#F2F4F8")
    ax.set_ylabel("Weekday", color="#F2F4F8")

    ax.set_xticks(range(len(heatmap_table.columns)))
    ax.set_xticklabels(heatmap_table.columns, color="#F2F4F8")

    ax.set_yticks(range(len(heatmap_table.index)))
    ax.set_yticklabels(heatmap_table.index, color="#F2F4F8")

    ax.tick_params(axis="x", colors="#F2F4F8")
    ax.tick_params(axis="y", colors="#F2F4F8")

    colorbar = fig.colorbar(heatmap, ax=ax)
    colorbar.set_label("Violation Count", color="#F2F4F8")
    colorbar.ax.yaxis.set_tick_params(color="#F2F4F8")

    for label in colorbar.ax.get_yticklabels():
        label.set_color("#F2F4F8")

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)


# Vehicle Analysis
if selected_page == "🚘 Vehicle Analysis":

    st.title("🚘 Vehicle Analysis")
    st.write("This section shows which vehicle types, makes, models, and colors are most involved in traffic violations.")

    def format_thousands(x, pos):
        return f"{int(x / 1000)}k"

    vehicle_col1, vehicle_col2 = st.columns(2)


    # Chart 1: Top 15 Vehicle Makes
    with vehicle_col1:
        st.markdown("### Top 15 Vehicle Makes")

        top_makes = filtered_df["Make"].value_counts().head(15)

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.barh(
            top_makes.index,
            top_makes.values,
            color="#4C78A8"
        )

        ax.set_xlabel("Count", color="#F2F4F8")
        ax.set_ylabel("Make", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8")
        ax.tick_params(axis="y", colors="#F2F4F8", labelsize=8)

        ax.xaxis.set_major_formatter(FuncFormatter(format_thousands))

        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)
       
        fig.subplots_adjust(left=0.22, right=0.95, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    # Chart 2: Top 15 Vehicle Models
    with vehicle_col2:
        st.markdown("### Top 15 Vehicle Models")

        top_models = filtered_df["Model"].value_counts().head(15)

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.barh(
            top_models.index,
            top_models.values,
            color="#2E8B57"
        )

        ax.set_xlabel("Count", color="#F2F4F8")
        ax.set_ylabel("Model", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8")
        ax.tick_params(axis="y", colors="#F2F4F8", labelsize=8)

        ax.xaxis.set_major_formatter(FuncFormatter(format_thousands))

        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)
       
        fig.subplots_adjust(left=0.22, right=0.95, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    st.divider()

    vehicle_col3, vehicle_col4 = st.columns(2)


    # Chart 3: Vehicle Colors
    with vehicle_col3:
        st.markdown("### Vehicle Colors")

        top_colors = filtered_df["Color"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.bar(
            top_colors.index,
            top_colors.values,
            color="#6C63FF"
        )

        ax.set_xlabel("Color", color="#F2F4F8")
        ax.set_ylabel("Count", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8", rotation=35)
        ax.tick_params(axis="y", colors="#F2F4F8")

        ax.yaxis.set_major_formatter(FuncFormatter(format_thousands))

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.grid(axis="y", alpha=0.2)

        fig.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.28)

        st.pyplot(fig, use_container_width=True)


    # Chart 4: Vehicle Types
    with vehicle_col4:
        st.markdown("### Vehicle Types")

        vehicle_type_counts = filtered_df["VehicleType"].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        fig.patch.set_edgecolor("black")
        fig.patch.set_linewidth(1)

        ax.set_facecolor("#0E1117")

        wedges, texts, autotexts = ax.pie(
            vehicle_type_counts.values,
            labels=None,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.75,
            radius=0.90,
            wedgeprops={"width": 0.35},
            textprops={"color": "#F2F4F8", "fontsize": 8}
        )

        legend = ax.legend(
            wedges,
            vehicle_type_counts.index,
            title="Vehicle Type",
            loc="center left",
            bbox_to_anchor=(0.95, 0.5),
            frameon=False,
            labelcolor="#F2F4F8"
        )

        legend.get_title().set_color("#F2F4F8")

        ax.set_aspect("equal")

        ax.set_xlim(-1.15, 1.75)
        ax.set_ylim(-1.00, 1.00)

        fig.subplots_adjust(left=0.05, right=0.85, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    st.divider()


    # Chart 5: Accident Rate by Top Vehicle Makes
    st.markdown("### 🚨 Accident Rate by Top Vehicle Makes")

    top_make_names = filtered_df["Make"].value_counts().head(15).index

    make_df = filtered_df[filtered_df["Make"].isin(top_make_names)]

    accident_rate = (
        make_df
        .groupby("Make")["Accident"]
        .mean()
        .sort_values(ascending=False)
        * 100
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    fig.patch.set_facecolor("#0E1117")
    ax.set_facecolor("#0E1117")

    ax.barh(
        accident_rate.index,
        accident_rate.values,
        color="#D62728"
    )

    ax.set_xlabel("Accident Rate (%)", color="#F2F4F8")
    ax.set_ylabel("Make", color="#F2F4F8")

    ax.tick_params(axis="x", colors="#F2F4F8")
    ax.tick_params(axis="y", colors="#F2F4F8")

    def format_percent(x, pos):
        return f"{x:.1f}%"

    ax.xaxis.set_major_formatter(FuncFormatter(format_percent))

    ax.invert_yaxis()

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)


# Demographic Analysis
if selected_page == "👥 Demographic Analysis":

    st.title("👥 Demographic Analysis")
    st.write("This section analyzes violation patterns based on driver gender and race.")

    def format_thousands(x, pos):
        return f"{int(x / 1000)}k"

    def format_percent(x, pos):
        return f"{x:.1f}%"

    demo_col1, demo_col2 = st.columns(2)


    # Chart 1: Violations by Gender
    with demo_col1:
        st.markdown("### Violations by Gender")

        gender_counts = filtered_df["Gender"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.bar(
            gender_counts.index,
            gender_counts.values,
            color="#4C78A8"
        )

        ax.set_xlabel("Gender", color="#F2F4F8")
        ax.set_ylabel("Count", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8")
        ax.tick_params(axis="y", colors="#F2F4F8")

        ax.yaxis.set_major_formatter(FuncFormatter(format_thousands))

        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    # Chart 2: Violations by Race
    with demo_col2:
        st.markdown("### Violations by Race")

        race_counts = filtered_df["Race"].value_counts()

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.barh(
            race_counts.index,
            race_counts.values,
            color="#6C63FF"
        )

        ax.set_xlabel("Count", color="#F2F4F8")
        ax.set_ylabel("Race", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8")
        ax.tick_params(axis="y", colors="#F2F4F8", labelsize=8)

        ax.xaxis.set_major_formatter(FuncFormatter(format_thousands))

        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.subplots_adjust(left=0.22, right=0.95, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    st.divider()

    demo_col3, demo_col4 = st.columns(2)


    # Chart 3: Accident Rate by Gender
    with demo_col3:
        st.markdown("### Accident Rate by Gender")

        accident_rate_gender = (
            filtered_df
            .groupby("Gender")["Accident"]
            .mean()
            .sort_values(ascending=False)
            * 100
        )

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.bar(
            accident_rate_gender.index,
            accident_rate_gender.values,
            color="#D08159"
        )

        ax.set_xlabel("Gender", color="#F2F4F8")
        ax.set_ylabel("Accident Rate %", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8")
        ax.tick_params(axis="y", colors="#F2F4F8")

        ax.yaxis.set_major_formatter(FuncFormatter(format_percent))

        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)


    # Chart 4: Accident Rate by Race
    with demo_col4:
        st.markdown("### Accident Rate by Race")

        accident_rate_race = (
            filtered_df
            .groupby("Race")["Accident"]
            .mean()
            .sort_values(ascending=False)
            * 100
        )

        fig, ax = plt.subplots(figsize=(7, 4))

        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")

        ax.barh(
            accident_rate_race.index,
            accident_rate_race.values,
            color="#D95F02"
        )

        ax.set_xlabel("Accident Rate %", color="#F2F4F8")
        ax.set_ylabel("Race", color="#F2F4F8")

        ax.tick_params(axis="x", colors="#F2F4F8")
        ax.tick_params(axis="y", colors="#F2F4F8", labelsize=8)

        ax.xaxis.set_major_formatter(FuncFormatter(format_percent))

        ax.invert_yaxis()

        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.subplots_adjust(left=0.22, right=0.95, top=0.90, bottom=0.18)

        st.pyplot(fig, use_container_width=True)