from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.ingestion_schema import (
    IngestionRequest
)

from app.services.ingestion_service import (
    ingest_state_climate_data
)


router = APIRouter()


@router.post("/ingest")
def ingest_data(
    payload: IngestionRequest,
    db: Session = Depends(get_db)
):

    result = ingest_state_climate_data(
        db=db,
        state=payload.state,
        start_year=payload.start_year,
        end_year=payload.end_year
    )

    return {
        "success": True,
        "data": result
    }