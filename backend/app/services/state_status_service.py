from sqlalchemy.orm import Session

from app.models.state_status import StateStatus


def create_or_update_state_status(
    db: Session,
    state: str,
    ingested: bool = False,
    trained: bool = False,
    analysed: bool = False
):

    existing = (
        db.query(StateStatus)
        .filter(StateStatus.state == state)
        .first()
    )

    if existing:

        existing.ingested = ingested
        existing.trained = trained
        existing.analysed = analysed

    else:

        status = StateStatus(
            state=state,
            ingested=ingested,
            trained=trained,
            analysed=analysed
        )

        db.add(status)

    db.commit()