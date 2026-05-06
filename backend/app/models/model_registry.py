from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text
)

from datetime import datetime

from app.database.base import Base


class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)

    state = Column(String, nullable=False)

    variable = Column(String, nullable=False)

    model_type = Column(String, nullable=False)

    model_path = Column(String, nullable=False)

    rmse = Column(Float)
    mae = Column(Float)
    mape = Column(Float)

    best_params = Column(Text)

    trained_on_start = Column(Integer)
    trained_on_end = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)