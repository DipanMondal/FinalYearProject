import numpy as np
import pandas as pd


def generate_future_months(
    last_year: int,
    last_month: int,
    horizon: int
):

    future_rows = []

    current_year = last_year
    current_month = last_month

    for _ in range(horizon):

        current_month += 1

        if current_month > 12:

            current_month = 1
            current_year += 1

        future_rows.append({
            "year": current_year,
            "month": current_month
        })

    return pd.DataFrame(future_rows)
    
    
    
def generate_future_exog_features(
    future_df: pd.DataFrame
):

    future_df["seasonal_sin"] = np.sin(
        2 * np.pi * future_df["month"] / 12
    )

    future_df["seasonal_cos"] = np.cos(
        2 * np.pi * future_df["month"] / 12
    )

    return future_df