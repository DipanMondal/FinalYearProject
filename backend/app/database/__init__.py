from app.database.base import Base
from app.database.session import engine

# Import models
from app.models.metadata import Metadata
from app.models.climate_data import ClimateData
from app.models.state_status import StateStatus


def init_db():
    Base.metadata.create_all(bind=engine)