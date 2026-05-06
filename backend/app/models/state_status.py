from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class StateStatus(Base):
    __tablename__ = "state_status"

    state = Column(String, primary_key=True)

    ingested = Column(Boolean, default=False)
    trained = Column(Boolean, default=False)
    analysed = Column(Boolean, default=False)

    ingestion_in_progress = Column(Boolean, default=False)
    training_in_progress = Column(Boolean, default=False)
    analysis_in_progress = Column(Boolean, default=False)

    ingestion_failed = Column(Boolean, default=False)
    training_failed = Column(Boolean, default=False)
    analysis_failed = Column(Boolean, default=False)

    last_updated = Column(DateTime, default=datetime.utcnow)