from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True)

    state = Column(String, unique=True, nullable=False)

    report_path = Column(String, nullable=False)

    warming_rate = Column(Float)

    rainfall_trend = Column(Float)

    anomaly_score = Column(Float)

    generated_at = Column(DateTime, default=datetime.utcnow)