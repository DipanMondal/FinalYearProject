from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class EngineeredFeatures(Base):
    __tablename__ = "engineered_features"

    id = Column(Integer, primary_key=True, index=True)

    state = Column(String, nullable=False)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    
    avg_temperature = Column(Float)

    rainfall = Column(Float)

    humidity = Column(Float)

    temp_anomaly = Column(Float)
    rainfall_anomaly = Column(Float)
    humidity_anomaly = Column(Float)

    temp_rolling_3 = Column(Float)
    temp_rolling_6 = Column(Float)

    rainfall_rolling_3 = Column(Float)

    humidity_rolling_3 = Column(Float)

    temp_lag_1 = Column(Float)
    temp_lag_3 = Column(Float)

    seasonal_sin = Column(Float)
    seasonal_cos = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)