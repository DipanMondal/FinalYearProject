from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    UniqueConstraint
)

from datetime import datetime

from app.database.base import Base


class ClimateData(Base):
    __tablename__ = "climate_data"

    id = Column(Integer, primary_key=True, index=True)

    state = Column(String, nullable=False)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)

    avg_temperature = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "state",
            "year",
            "month",
            name="unique_state_year_month"
        ),
    )