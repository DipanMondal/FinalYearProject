from sqlalchemy.orm import Session

from app.models.state_status import StateStatus


def get_all_states(db: Session):

    return db.query(StateStatus).all()