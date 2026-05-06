import pandas as pd

from sqlalchemy.orm import Session

from app.models.engineered_features import (
    EngineeredFeatures
)

from app.models.model_registry import (
    ModelRegistry
)

from app.utils.model_utils import (
    load_model
)

from app.utils.recursive_features import (

    compute_seasonal_features,

    compute_temperature_features,

    compute_rainfall_features,

    compute_humidity_features
)


def load_historical_dataframe(
    db: Session,
    state: str
):

    rows = (

        db.query(EngineeredFeatures)

        .filter(
            EngineeredFeatures.state == state
        )

        .order_by(
            EngineeredFeatures.year,

            EngineeredFeatures.month
        )

        .all()
    )

    data = []

    for row in rows:

        data.append({

            "year": row.year,
            "month": row.month,

            "avg_temperature":
                row.avg_temperature,

            "rainfall":
                row.rainfall,

            "humidity":
                row.humidity
        })

    return pd.DataFrame(data)


def load_state_model(
    db: Session,
    state: str,
    variable: str
):

    entry = (

        db.query(ModelRegistry)

        .filter(
            ModelRegistry.state == state,

            ModelRegistry.variable == variable
        )

        .first()
    )

    if not entry:

        raise ValueError(
            f"No model found for {variable}"
        )

    return load_model(entry.model_path)


def recursive_forecast_variable(

    db: Session,

    state: str,

    variable: str,

    horizon: int
):

    model = load_state_model(

        db=db,

        state=state,

        variable=variable
    )

    current_df = load_historical_dataframe(

        db=db,

        state=state
    )

    forecast_results = []

    for _ in range(horizon):

        last_row = current_df.iloc[-1]

        next_month = int(last_row["month"]) + 1
        next_year = int(last_row["year"])

        if next_month > 12:

            next_month = 1
            next_year += 1

        seasonal_sin, seasonal_cos = (
            compute_seasonal_features(
                next_month
            )
        )

        if variable == "avg_temperature":

            features = (
                compute_temperature_features(
                    current_df
                )
            )

        elif variable == "rainfall":

            features = (
                compute_rainfall_features(
                    current_df
                )
            )

        else:

            features = (
                compute_humidity_features(
                    current_df
                )
            )

        exog = pd.DataFrame([{

            **features,

            "seasonal_sin":
                seasonal_sin,

            "seasonal_cos":
                seasonal_cos
        }])

        prediction = model.forecast(

            steps=1,

            exog=exog
        )

        predicted_value = (
            float(prediction.iloc[0])
        )

        forecast_results.append({

            "year": next_year,

            "month": next_month,

            "prediction":
                predicted_value
        })

        new_row = {

            "year": next_year,

            "month": next_month,

            "avg_temperature":
                last_row["avg_temperature"],

            "rainfall":
                last_row["rainfall"],

            "humidity":
                last_row["humidity"]
        }

        new_row[variable] = predicted_value

        current_df = pd.concat([

            current_df,

            pd.DataFrame([new_row])

        ], ignore_index=True)

    return forecast_results


def forecast_state(
    db: Session,
    state: str,
    horizon: int
):

    return {

        "avg_temperature":
            recursive_forecast_variable(

                db=db,

                state=state,

                variable="avg_temperature",

                horizon=horizon
            ),

        "rainfall":
            recursive_forecast_variable(

                db=db,

                state=state,

                variable="rainfall",

                horizon=horizon
            ),

        "humidity":
            recursive_forecast_variable(

                db=db,

                state=state,

                variable="humidity",

                horizon=horizon
            )
    }