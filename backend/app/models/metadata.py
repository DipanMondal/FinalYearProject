from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database.base import Base


class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)

    state = Column(String, unique=True, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    source = Column(String, nullable=False)

    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)

    records_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)