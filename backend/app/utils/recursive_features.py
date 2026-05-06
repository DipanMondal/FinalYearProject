import numpy as np


def compute_seasonal_features(
    month: int
):

    seasonal_sin = np.sin(
        2 * np.pi * month / 12
    )

    seasonal_cos = np.cos(
        2 * np.pi * month / 12
    )

    return seasonal_sin, seasonal_cos


def compute_temperature_features(df):

    latest = df.tail(6)

    return {

        "temp_rolling_3":
            latest["avg_temperature"]
            .tail(3)
            .mean(),

        "temp_rolling_6":
            latest["avg_temperature"]
            .mean(),

        "temp_lag_1":
            latest["avg_temperature"]
            .iloc[-1],

        "temp_lag_3":
            latest["avg_temperature"]
            .iloc[-3]
    }


def compute_rainfall_features(df):

    latest = df.tail(3)

    return {

        "rainfall_rolling_3":
            latest["rainfall"]
            .mean(),

        "rainfall_lag_1":
            latest["rainfall"]
            .iloc[-1],

        "rainfall_lag_3":
            latest["rainfall"]
            .iloc[-3]
    }


def compute_humidity_features(df):

    latest = df.tail(3)

    return {

        "humidity_rolling_3":
            latest["humidity"]
            .mean(),

        "humidity_lag_1":
            latest["humidity"]
            .iloc[-1],

        "humidity_lag_3":
            latest["humidity"]
            .iloc[-3]
    }