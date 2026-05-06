import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from statsmodels.tsa.statespace.sarimax import (
    SARIMAX
)

from sqlalchemy.orm import Session

from app.models.engineered_features import (
    EngineeredFeatures
)

from app.models.model_registry import (
    ModelRegistry
)

from app.services.pipeline_logger_service import (
    log_pipeline_event
)

from app.utils.model_utils import (
    save_model
)

from app.core.model_config import (
    SARIMAX_CONFIG
)

from app.services.state_status_service import (
    create_or_update_state_status
)


# Loading the feature data from db
def load_feature_dataframe(
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
                row.humidity,

            "temp_anomaly": row.temp_anomaly,

            "rainfall_anomaly":
                row.rainfall_anomaly,

            "humidity_anomaly":
                row.humidity_anomaly,

            "temp_rolling_3":
                row.temp_rolling_3,

            "temp_rolling_6":
                row.temp_rolling_6,
                
            "rainfall_rolling_3":
                row.rainfall_rolling_3,

            "humidity_rolling_3":
                row.humidity_rolling_3,

            "temp_lag_1":
                row.temp_lag_1,

            "temp_lag_3":
                row.temp_lag_3,
                
            "rainfall_lag_1":
                row.rainfall_lag_1,

            "rainfall_lag_3":
                row.rainfall_lag_3,

            "humidity_lag_1":
                row.humidity_lag_1,

            "humidity_lag_3":
                row.humidity_lag_3,

            "seasonal_sin":
                row.seasonal_sin,

            "seasonal_cos":
                row.seasonal_cos
        })

    return pd.DataFrame(data)
    
    
# Training a single SARIMAX model
def train_sarimax_model(
    y_train,
    exog_train,
    order,
    seasonal_order
):

    model = SARIMAX(

        y_train,

        exog=exog_train,

        order=order,

        seasonal_order=seasonal_order,

        enforce_stationarity=False,
        enforce_invertibility=False
    )

    fitted_model = model.fit(
        disp=False
    )

    return fitted_model
    
    
# Grid Search CV
def grid_search_sarimax(
    y_train,
    y_test,
    exog_train,
    exog_test
):

    best_model = None

    best_rmse = np.inf

    best_order = None
    best_seasonal_order = None

    for order in SARIMAX_CONFIG["order_grid"]:

        for seasonal_order in (
            SARIMAX_CONFIG[
                "seasonal_order_grid"
            ]
        ):

            try:

                model = train_sarimax_model(

                    y_train=y_train,
                    exog_train=exog_train,

                    order=order,

                    seasonal_order=seasonal_order
                )

                predictions = model.predict(

                    start=len(y_train),

                    end=(
                        len(y_train)
                        + len(y_test)
                        - 1
                    ),

                    exog=exog_test
                )

                rmse = np.sqrt(

                    mean_squared_error(
                        y_test,
                        predictions
                    )
                )

                if rmse < best_rmse:

                    best_rmse = rmse

                    best_model = model

                    best_order = order

                    best_seasonal_order = (
                        seasonal_order
                    )

            except Exception:

                continue

    return {
        "model": best_model,
        "rmse": best_rmse,
        "order": best_order,
        "seasonal_order":
            best_seasonal_order
    }
    
 
# Training Loop
def train_state_variable_model(
    db: Session,
    state: str,
    target_column: str
):

    df = load_feature_dataframe(
        db=db,
        state=state
    )

    df = df.dropna()

    if len(df) < 24:

        raise ValueError(
            "Not enough data for training"
        )

    if target_column == "avg_temperature":

        exogenous_columns = [

            "temp_rolling_3",
            "temp_rolling_6",

            "temp_lag_1",
            "temp_lag_3",

            "seasonal_sin",
            "seasonal_cos"
        ]

    elif target_column == "rainfall":

        exogenous_columns = [

            "rainfall_rolling_3",

            "rainfall_lag_1",
            "rainfall_lag_3",

            "seasonal_sin",
            "seasonal_cos"
        ]

    else:

        exogenous_columns = [

            "humidity_rolling_3",

            "humidity_lag_1",
            "humidity_lag_3",

            "seasonal_sin",
            "seasonal_cos"
        ]

    y = df[target_column]

    X = df[exogenous_columns]

    split_index = int(
        len(df) * 0.8
    )

    y_train = y[:split_index]
    y_test = y[split_index:]

    X_train = X[:split_index]
    X_test = X[split_index:]

    grid_result = grid_search_sarimax(

        y_train=y_train,
        y_test=y_test,

        exog_train=X_train,
        exog_test=X_test
    )

    best_model = grid_result["model"]

    predictions = best_model.predict(

        start=len(y_train),

        end=(
            len(y_train)
            + len(y_test)
            - 1
        ),

        exog=X_test
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    model_path = save_model(

        model=best_model,

        state=state,

        variable=target_column
    )

    registry_entry = ModelRegistry(

        state=state,

        variable=target_column,

        model_type="SARIMAX",

        model_path=model_path,

        rmse=float(rmse),

        mae=float(mae),

        best_params=str({
            "order":
                grid_result["order"],

            "seasonal_order":
                grid_result[
                    "seasonal_order"
                ]
        })
    )

    db.add(registry_entry)

    db.commit()

    log_pipeline_event(

        db=db,

        state=state,

        pipeline="TRAINING",

        status="SUCCESS",

        message=(
            f"{target_column} model "
            f"trained successfully"
        )
    )

    return {

        "state": state,

        "variable": target_column,

        "rmse": rmse,

        "mae": mae
    }
    
    
# train all state models
def train_all_models_for_state(
    db: Session,
    state: str
):

    results = []


    targets = [
        "avg_temperature",
        "rainfall",
        "humidity"
    ]
    

    for target in targets:

        result = train_state_variable_model(

            db=db,

            state=state,

            target_column=target
        )

        results.append(result)
        
    create_or_update_state_status(

        db=db,

        state=state,

        ingested=True,

        trained=True
    )

    return results
    
    
