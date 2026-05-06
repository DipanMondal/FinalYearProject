from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.services.state_service import get_all_states


router = APIRouter()


@router.get("/states")
def get_states(
    db: Session = Depends(get_db)
):

    states = get_all_states(db)

    result = []

    for state in states:

        result.append({
            "state": state.state,
            "ingested": state.ingested,
            "trained": state.trained,
            "analysed": state.analysed
        })

    return result