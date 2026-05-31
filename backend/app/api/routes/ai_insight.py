import json
from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException

from app.core.config import settings
from app.services.ai_analysis_service import AI_INSIGHT_FILENAME


router = APIRouter()


@router.get("/ai-insight/{state}")
def get_ai_insight_report(
    state: str
):

    report_path = (
        Path(settings.ARTIFACTS_DIR)
        / state
        / AI_INSIGHT_FILENAME
    )

    if not report_path.exists():

        raise HTTPException(
            status_code=404,
            detail="AI insight report not found. Regenerate analysis first."
        )

    with open(report_path, "r", encoding="utf-8") as f:

        report = json.load(f)

    return report