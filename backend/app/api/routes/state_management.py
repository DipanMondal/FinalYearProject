from pathlib import Path

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.models.metadata import Metadata

from app.models.engineered_features import (
    EngineeredFeatures
)

from app.models.model_registry import (
    ModelRegistry
)

from app.models.analysis_report import (
    AnalysisReport
)

from app.models.state_status import (
    StateStatus
)

from app.models.climate_data import (
    ClimateData
)

from app.services.state_status_service import (
    update_trained_status,
    update_analysed_status
)


router = APIRouter()


# -----------------------------------
# DELETE STATE DATA
# -----------------------------------

@router.delete("/state/{state}")
def delete_state(
    state: str,
    db: Session = Depends(get_db)
):

    db.query(Metadata).filter(
        Metadata.state == state
    ).delete()

    db.query(EngineeredFeatures).filter(
        EngineeredFeatures.state == state
    ).delete()

    db.query(StateStatus).filter(
        StateStatus.state == state
    ).delete()
    
    db.query(ClimateData).filter(
        ClimateData.state == state
    ).delete()
    
    delete_models(db = db, state = state)
    delete_analysis(db = db, state = state)

    db.commit()

    return {
        "success": True,
        "message": (
            f"{state} data deleted"
        )
    }


# -----------------------------------
# DELETE MODELS
# -----------------------------------

@router.delete("/models/{state}")
def delete_models(
    state: str,
    db: Session = Depends(get_db)
):

    models = (

        db.query(ModelRegistry)

        .filter(
            ModelRegistry.state == state
        )

        .all()
    )

    for model in models:

        model_path = Path(
            model.model_path
        )
        
        if model_path.exists():

            model_path.unlink()

        db.delete(model)
        
    update_trained_status(
        db = db,
        
        state = state,
    
        value = False
    )

    db.commit()

    return {
        "success": True,
        "message": (
            f"{state} models deleted"
        )
    }


# -----------------------------------
# DELETE ANALYSIS
# -----------------------------------

@router.delete("/analysis/{state}")
def delete_analysis(
    state: str,
    db: Session = Depends(get_db)
):

    reports = (

        db.query(AnalysisReport)

        .filter(
            AnalysisReport.state == state
        )

        .all()
    )

    for report in reports:

        report_path = Path(
            report.report_path
        )

        if report_path.exists():

            report_path.unlink()

        db.delete(report)
        
    update_analysed_status(
        db = db,
        
        state = state,
        
        value = False
    )

    db.commit()

    return {
        "success": True,
        "message": (
            f"{state} analysis deleted"
        )
    }