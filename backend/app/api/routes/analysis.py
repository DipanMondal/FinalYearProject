from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.services.analysis_service import (
    generate_analysis_report
)

router = APIRouter()


@router.post("/analysis/{state}")
def run_analysis(
    state: str,
    db: Session = Depends(get_db)
):

    result = generate_analysis_report(

        db=db,

        state=state
    )

    return {
        "success": True,
        "data": result
    }