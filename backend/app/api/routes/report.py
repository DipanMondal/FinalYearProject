import json

from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException

from app.core.config import settings


router = APIRouter()


@router.get("/report/{state}")
def get_analysis_report(
    state: str
):

    report_path = (

        Path(settings.ARTIFACTS_DIR)

        / state

        / "analysis_report.json"
    )

    if not report_path.exists():

        raise HTTPException(

            status_code=404,

            detail=(
                "Analysis report not found"
            )
        )

    with open(report_path, "r") as f:

        report = json.load(f)

    return report