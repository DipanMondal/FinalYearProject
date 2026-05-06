from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class ForecastHistory(Base):
    __tablename__ = "forecast_history"

    id = Column(Integer, primary_key=True, index=True)

    state = Column(String)

    variable = Column(String)

    horizon = Column(Integer)

    forecast_path = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)