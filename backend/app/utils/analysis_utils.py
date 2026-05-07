import pandas as pd
import numpy as np

from scipy.stats import linregress


MONTH_NAMES = [

    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",

    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]


def generate_seasonal_signature(
    df: pd.DataFrame,
    value_column: str
):

    seasonal_data = {}

    years = sorted(
        df["year"].unique()
    )

    for year in years:

        yearly_df = (
            df[df["year"] == year]
            .sort_values("month")
        )

        monthly_values = []

        for month in range(1, 13):

            month_df = yearly_df[
                yearly_df["month"] == month
            ]

            if month_df.empty:

                monthly_values.append(None)

            else:

                value = (
                    month_df.iloc[0][value_column]
                )

                monthly_values.append(
                    float(value)
                )

        seasonal_data[str(year)] = (
            monthly_values
        )

    return seasonal_data


def generate_climatology(
    df: pd.DataFrame,
    value_column: str
):

    climatology = []

    for month in range(1, 13):

        month_df = df[
            df["month"] == month
        ]

        mean_value = (
            month_df[value_column]
            .mean()
        )

        climatology.append(
            float(mean_value)
        )

    return climatology
    
    
def generate_yearly_aggregation(
    df: pd.DataFrame
):

    yearly_df = (

        df.groupby("year")

        .agg({

            "avg_temperature": "mean",

            "rainfall": "mean",

            "humidity": "mean"
        })

        .reset_index()
    )

    return yearly_df
    
    
# Trend analysis function
def calculate_trend_analysis(
    yearly_df: pd.DataFrame,
    value_column: str
):

    x = yearly_df["year"].values

    y = yearly_df[value_column].values

    regression = linregress(x, y)

    slope = regression.slope

    intercept = regression.intercept

    r_squared = regression.rvalue ** 2

    p_value = regression.pvalue

    trend_per_decade = slope * 10

    return {

        "slope_per_year":
            float(slope),

        "trend_per_decade":
            float(trend_per_decade),

        "intercept":
            float(intercept),

        "r_squared":
            float(r_squared),

        "p_value":
            float(p_value)
    }
    
    
# Decadal Aggregation
def generate_decadal_analysis(
    yearly_df: pd.DataFrame
):

    yearly_df["decade"] = (

        yearly_df["year"] // 10
    ) * 10

    decadal_df = (

        yearly_df.groupby("decade")

        .agg({

            "avg_temperature": "mean",

            "rainfall": "mean",

            "humidity": "mean"
        })

        .reset_index()
    )

    results = []

    for _, row in decadal_df.iterrows():

        results.append({

            "decade":
                int(row["decade"]),

            "avg_temperature":
                float(row["avg_temperature"]),

            "rainfall":
                float(row["rainfall"]),

            "humidity":
                float(row["humidity"])
        })

    return results
    
    
# EXTREME YEAR ANALYSIS
def identify_extreme_years(
    yearly_df: pd.DataFrame
):

    hottest_year = yearly_df.loc[
        yearly_df["avg_temperature"].idxmax()
    ]

    coldest_year = yearly_df.loc[
        yearly_df["avg_temperature"].idxmin()
    ]

    wettest_year = yearly_df.loc[
        yearly_df["rainfall"].idxmax()
    ]

    driest_year = yearly_df.loc[
        yearly_df["rainfall"].idxmin()
    ]

    return {

        "hottest_year": {

            "year":
                int(hottest_year["year"]),

            "temperature":
                float(
                    hottest_year[
                        "avg_temperature"
                    ]
                )
        },

        "coldest_year": {

            "year":
                int(coldest_year["year"]),

            "temperature":
                float(
                    coldest_year[
                        "avg_temperature"
                    ]
                )
        },

        "wettest_year": {

            "year":
                int(wettest_year["year"]),

            "rainfall":
                float(
                    wettest_year[
                        "rainfall"
                    ]
                )
        },

        "driest_year": {

            "year":
                int(driest_year["year"]),

            "rainfall":
                float(
                    driest_year[
                        "rainfall"
                    ]
                )
        }
    }
    
    
# Heat wave detection
def detect_heatwaves(
    df: pd.DataFrame
):

    threshold = (
        df["avg_temperature"]
        .quantile(0.95)
    )

    heatwave_df = df[
        df["avg_temperature"] > threshold
    ]

    events = []

    for _, row in heatwave_df.iterrows():

        events.append({

            "year":
                int(row["year"]),

            "month":
                int(row["month"]),

            "temperature":
                float(
                    row["avg_temperature"]
                )
        })

    return {

        "threshold":
            float(threshold),

        "event_count":
            len(events),

        "events":
            events
    }
    
    
# EXTREME RAINFALL DETECTION
def detect_extreme_rainfall(
    df: pd.DataFrame
):

    threshold = (
        df["rainfall"]
        .quantile(0.95)
    )

    rainfall_df = df[
        df["rainfall"] > threshold
    ]

    events = []

    for _, row in rainfall_df.iterrows():

        events.append({

            "year":
                int(row["year"]),

            "month":
                int(row["month"]),

            "rainfall":
                float(row["rainfall"])
        })

    return {

        "threshold":
            float(threshold),

        "event_count":
            len(events),

        "events":
            events
    }


# HIGH HUMIDITY EVENTS
def detect_high_humidity_events(
    df: pd.DataFrame
):

    threshold = (
        df["humidity"]
        .quantile(0.95)
    )

    humidity_df = df[
        df["humidity"] > threshold
    ]

    events = []

    for _, row in humidity_df.iterrows():

        events.append({

            "year":
                int(row["year"]),

            "month":
                int(row["month"]),

            "humidity":
                float(row["humidity"])
        })

    return {

        "threshold":
            float(threshold),

        "event_count":
            len(events),

        "events":
            events
    } 


# Volatality
def calculate_volatility_analysis(
    df: pd.DataFrame
):

    temperature_volatility = (
        df["avg_temperature"]
        .std()
    )

    rainfall_volatility = (
        df["rainfall"]
        .std()
    )

    humidity_volatility = (
        df["humidity"]
        .std()
    )

    return {

        "temperature_volatility":
            float(
                temperature_volatility
            ),

        "rainfall_volatility":
            float(
                rainfall_volatility
            ),

        "humidity_volatility":
            float(
                humidity_volatility
            )
    }


# ANOMALY FREQUENCY ANALYSIS
def calculate_anomaly_frequency(
    df: pd.DataFrame
):

    temp_threshold = (
        df["temp_anomaly"]
        .std()
    )

    rainfall_threshold = (
        df["rainfall_anomaly"]
        .std()
    )

    humidity_threshold = (
        df["humidity_anomaly"]
        .std()
    )

    temp_events = df[
        abs(df["temp_anomaly"])
        > temp_threshold
    ]

    rainfall_events = df[
        abs(df["rainfall_anomaly"])
        > rainfall_threshold
    ]

    humidity_events = df[
        abs(df["humidity_anomaly"])
        > humidity_threshold
    ]

    return {

        "temperature_anomaly_events":
            len(temp_events),

        "rainfall_anomaly_events":
            len(rainfall_events),

        "humidity_anomaly_events":
            len(humidity_events)
    }    
  