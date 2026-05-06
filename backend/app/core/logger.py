from loguru import logger
from pathlib import Path

from app.core.config import settings


Path(settings.LOGS_DIR).mkdir(parents=True, exist_ok=True)

logger.add(
    f"{settings.LOGS_DIR}/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO"
)