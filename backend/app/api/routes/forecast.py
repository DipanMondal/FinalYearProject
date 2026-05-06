from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.forecast_service import (
    forecast_state
)


router = APIRouter()


@router.get("/forecast/{state}")
def forecast(
    state: str,
    horizon: int,
    db: Session = Depends(get_db)
):

    result = forecast_state(

        db=db,

        state=state,

        horizon=horizon
    )

    return {
        "success": True,
        "data": result
    }