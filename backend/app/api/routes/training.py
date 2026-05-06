from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.training_service import (
    train_all_models_for_state
)


router = APIRouter()


@router.post("/train/{state}")
def train_models(
    state: str,
    db: Session = Depends(get_db)
):

    result = train_all_models_for_state(

        db=db,
        state=state
    )

    return {
        "success": True,
        "data": result
    }