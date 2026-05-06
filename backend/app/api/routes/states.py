from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.state_status import StateStatus

router = APIRouter()


@router.get("/states")
def get_states():

    db: Session = SessionLocal()

    states = db.query(StateStatus).all()

    result = []

    for state in states:
        result.append({
            "state": state.state,
            "ingested": state.ingested,
            "trained": state.trained,
            "analysed": state.analysed
        })

    db.close()

    return result