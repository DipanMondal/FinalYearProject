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
    
    

    