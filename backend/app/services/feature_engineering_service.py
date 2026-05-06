import numpy as np
import pandas as pd

from sqlalchemy.orm import Session

from app.models.climate_data import ClimateData
from app.models.engineered_features import (
    EngineeredFeatures
)


# Loading State Data
def load_state_climate_data(
    db: Session,
    state: str
):

    rows = (
        db.query(ClimateData)
        .filter(ClimateData.state == state)
        .order_by(
            ClimateData.year,
            ClimateData.month
        )
        .all()
    )

    data = []

    for row in rows:

        data.append({
            "year": row.year,
            "month": row.month,
            "avg_temperature": row.avg_temperature,
            "rainfall": row.rainfall,
            "humidity": row.humidity
        })

    df = pd.DataFrame(data)

    return df
    
    
# feature generation function
def generate_features(df: pd.DataFrame):

    # -----------------------------
    # Rolling Features
    # -----------------------------

    df["temp_rolling_3"] = (
        df["avg_temperature"]
        .rolling(window=3)
        .mean()
    )

    df["temp_rolling_6"] = (
        df["avg_temperature"]
        .rolling(window=6)
        .mean()
    )

    df["rainfall_rolling_3"] = (
        df["rainfall"]
        .rolling(window=3)
        .mean()
    )

    df["humidity_rolling_3"] = (
        df["humidity"]
        .rolling(window=3)
        .mean()
    )

    # -----------------------------
    # Lag Features
    # -----------------------------

    df["temp_lag_1"] = (
        df["avg_temperature"]
        .shift(1)
    )

    df["temp_lag_3"] = (
        df["avg_temperature"]
        .shift(3)
    )
    
    df["rainfall_lag_1"] = (
        df["rainfall"]
        .shift(1)
    )

    df["rainfall_lag_3"] = (
        df["rainfall"]
        .shift(3)
    )

    df["humidity_lag_1"] = (
        df["humidity"]
        .shift(1)
    )

    df["humidity_lag_3"] = (
        df["humidity"]
        .shift(3)
    )

    # -----------------------------
    # Seasonal Encoding
    # -----------------------------

    df["seasonal_sin"] = np.sin(
        2 * np.pi * df["month"] / 12
    )

    df["seasonal_cos"] = np.cos(
        2 * np.pi * df["month"] / 12
    )

    # -----------------------------
    # Monthly Baselines
    # -----------------------------

    monthly_temp_avg = (
        df.groupby("month")["avg_temperature"]
        .transform("mean")
    )

    monthly_rainfall_avg = (
        df.groupby("month")["rainfall"]
        .transform("mean")
    )

    monthly_humidity_avg = (
        df.groupby("month")["humidity"]
        .transform("mean")
    )

    # -----------------------------
    # Anomaly Features
    # -----------------------------

    df["temp_anomaly"] = (
        df["avg_temperature"]
        - monthly_temp_avg
    )

    df["rainfall_anomaly"] = (
        df["rainfall"]
        - monthly_rainfall_avg
    )

    df["humidity_anomaly"] = (
        df["humidity"]
        - monthly_humidity_avg
    )

    return df
    
   
# function to save generated feature in the database
def save_engineered_features(
    db: Session,
    state: str,
    df: pd.DataFrame
):

    for _, row in df.iterrows():

        feature_row = EngineeredFeatures(

            state=state,

            year=int(row["year"]),
            month=int(row["month"]),
            
            avg_temperature=float(
                row["avg_temperature"]
            ),

            rainfall=float(
                row["rainfall"]
            ),

            humidity=float(
                row["humidity"]
            ),

            temp_anomaly=float(row["temp_anomaly"]),

            rainfall_anomaly=float(
                row["rainfall_anomaly"]
            ),

            humidity_anomaly=float(
                row["humidity_anomaly"]
            ),

            temp_rolling_3=float(
                row["temp_rolling_3"]
            ) if pd.notna(row["temp_rolling_3"]) else None,

            temp_rolling_6=float(
                row["temp_rolling_6"]
            ) if pd.notna(row["temp_rolling_6"]) else None,

            rainfall_rolling_3=float(
                row["rainfall_rolling_3"]
            ) if pd.notna(row["rainfall_rolling_3"]) else None,

            humidity_rolling_3=float(
                row["humidity_rolling_3"]
            ) if pd.notna(row["humidity_rolling_3"]) else None,

            temp_lag_1=float(
                row["temp_lag_1"]
            ) if pd.notna(row["temp_lag_1"]) else None,

            temp_lag_3=float(
                row["temp_lag_3"]
            ) if pd.notna(row["temp_lag_3"]) else None,
            
            rainfall_lag_1=float(
                row["rainfall_lag_1"]
            ) if pd.notna(
                row["rainfall_lag_1"]
            ) else None,

            rainfall_lag_3=float(
                row["rainfall_lag_3"]
            ) if pd.notna(
                row["rainfall_lag_3"]
            ) else None,

            humidity_lag_1=float(
                row["humidity_lag_1"]
            ) if pd.notna(
                row["humidity_lag_1"]
            ) else None,

            humidity_lag_3=float(
                row["humidity_lag_3"]
            ) if pd.notna(
                row["humidity_lag_3"]
            ) else None,

            seasonal_sin=float(row["seasonal_sin"]),
            seasonal_cos=float(row["seasonal_cos"])
        )

        db.add(feature_row)

    db.commit()



#
# PIPELINE
#    
def generate_state_features(
    db: Session,
    state: str
):

    df = load_state_climate_data(
        db=db,
        state=state
    )

    if df.empty:

        raise ValueError(
            f"No climate data found for '{state}'"
        )

    featured_df = generate_features(df)

    save_engineered_features(
        db=db,
        state=state,
        df=featured_df
    )

    return {
        "state": state,
        "records_processed": len(featured_df)
    }