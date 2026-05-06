from app.database.base import Base
from app.database.session import engine

from app.models.metadata import Metadata
from app.models.climate_data import ClimateData
from app.models.state_status import StateStatus

from app.models.engineered_features import EngineeredFeatures
from app.models.model_registry import ModelRegistry
from app.models.analysis_report import AnalysisReport
from app.models.pipeline_log import PipelineLog
from app.models.forecast_history import ForecastHistory


def init_db():
    Base.metadata.create_all(bind=engine)