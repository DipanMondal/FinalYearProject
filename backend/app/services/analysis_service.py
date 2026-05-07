import json

from pathlib import Path

import pandas as pd

from sqlalchemy.orm import Session

from app.models.engineered_features import (
    EngineeredFeatures
)

from app.models.analysis_report import (
    AnalysisReport
)

from app.services.state_status_service import (
    create_or_update_state_status
)

from app.services.pipeline_logger_service import (
    log_pipeline_event
)

from app.core.config import settings

from app.utils.analysis_utils import (

    generate_seasonal_signature,

    generate_climatology,

    generate_yearly_aggregation,

    calculate_trend_analysis,

    generate_decadal_analysis,

    identify_extreme_years,

    detect_heatwaves,

    detect_extreme_rainfall,

    detect_high_humidity_events,

    calculate_volatility_analysis,

    calculate_anomaly_frequency,

    MONTH_NAMES
)


# Load analysis dataframe
def load_analysis_dataframe(
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

            "temp_anomaly":
                row.temp_anomaly,

            "rainfall_anomaly":
                row.rainfall_anomaly,

            "humidity_anomaly":
                row.humidity_anomaly
        })

    return pd.DataFrame(data)
    
    
# Create seasonal signature analysis
def create_seasonal_signature_analysis(
    df: pd.DataFrame
):

    temperature_signature = (
        generate_seasonal_signature(

            df=df,

            value_column="avg_temperature"
        )
    )

    rainfall_signature = (
        generate_seasonal_signature(

            df=df,

            value_column="rainfall"
        )
    )

    temperature_climatology = (
        generate_climatology(

            df=df,

            value_column="avg_temperature"
        )
    )

    rainfall_climatology = (
        generate_climatology(

            df=df,

            value_column="rainfall"
        )
    )

    return {

        "months": MONTH_NAMES,

        "temperature":
            temperature_signature,

        "rainfall":
            rainfall_signature,

        "temperature_climatology":
            temperature_climatology,

        "rainfall_climatology":
            rainfall_climatology
    }
    
    
# MAIN ANALYSIS PIPELINE
def generate_analysis_report(
    db: Session,
    state: str
):

    df = load_analysis_dataframe(

        db=db,

        state=state
    )

    if df.empty:

        raise ValueError(
            f"No analysis data for {state}"
        )

    seasonal_signature_analysis = (
        create_seasonal_signature_analysis(
            df
        )
    )
    
    yearly_df = generate_yearly_aggregation(
        df
    )
    
    temperature_trend = (
        calculate_trend_analysis(

            yearly_df,

            "avg_temperature"
        )
    )

    rainfall_trend = (
        calculate_trend_analysis(

            yearly_df,

            "rainfall"
        )
    )

    humidity_trend = (
        calculate_trend_analysis(

            yearly_df,

            "humidity"
        )
    )
    
    decadal_analysis = (
        generate_decadal_analysis(
            yearly_df
        )
    )
    
    extreme_years = (
        identify_extreme_years(
            yearly_df
        )
    )
    
    extreme_heatwaves = (
        detect_heatwaves(df)
    )

    extreme_rainfall = (
        detect_extreme_rainfall(df)
    )

    high_humidity_events = (
        detect_high_humidity_events(df)
    )

    volatility_analysis = (
        calculate_volatility_analysis(df)
    )

    anomaly_frequency = (
        calculate_anomaly_frequency(df)
    )
    
    report = {

        "state": state,

        "seasonal_signature":
            seasonal_signature_analysis,

        "trend_analysis": {

            "temperature":
                temperature_trend,

            "rainfall":
                rainfall_trend,

            "humidity":
                humidity_trend
        },

        "decadal_analysis":
            decadal_analysis,

        "extreme_years":
            extreme_years,
            
        "extreme_events": {

            "heatwaves":
                extreme_heatwaves,

            "extreme_rainfall":
                extreme_rainfall,

            "high_humidity":
                high_humidity_events
        },

        "volatility_analysis":
            volatility_analysis,

        "anomaly_frequency":
            anomaly_frequency,
    }

    # -----------------------------
    # Save Artifact
    # -----------------------------

    artifact_dir = (
        Path(settings.ARTIFACTS_DIR)
        / state
    )

    artifact_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = (
        artifact_dir
        / "analysis_report.json"
    )

    with open(report_path, "w") as f:

        json.dump(
            report,
            f,
            indent=4
        )

    # -----------------------------
    # Save Report Registry
    # -----------------------------

    report_entry = AnalysisReport(

        state=state,

        report_path=str(report_path)
    )

    db.add(report_entry)

    db.commit()

    # -----------------------------
    # Update State Status
    # -----------------------------

    create_or_update_state_status(

        db=db,

        state=state,

        analysed=True
    )

    # -----------------------------
    # Log Pipeline
    # -----------------------------

    log_pipeline_event(

        db=db,

        state=state,

        pipeline="ANALYSIS",

        status="SUCCESS",

        message=(
            "Analysis report generated"
        )
    )

    return report
    
    

