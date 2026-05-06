from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.feature_engineering_service import (
    generate_state_features
)


router = APIRouter()


@router.post("/features/{state}")
def create_features(
    state: str,
    db: Session = Depends(get_db)
):

    result = generate_state_features(
        db=db,
        state=state
    )

    return {
        "success": True,
        "data": result
    }