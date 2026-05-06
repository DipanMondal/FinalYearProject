from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from datetime import datetime

from app.database.base import Base


class PipelineLog(Base):
    __tablename__ = "pipeline_logs"

    id = Column(Integer, primary_key=True, index=True)

    state = Column(String)

    pipeline = Column(String)

    status = Column(String)

    message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)