from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.models.engineered_features import (
    EngineeredFeatures
)

router = APIRouter()


@router.get("/historical/{state}")
def get_historical_data(
    state: str,
    db: Session = Depends(get_db)
):

    rows = (

        db.query(EngineeredFeatures)

        .filter(
            EngineeredFeatures.state == state
        )

        .order_by(
            EngineeredFeatures.year,

            EngineeredFeatures.month
        )

        .all()
    )

    data = []

    for row in rows:

        data.append({

            "year": row.year,

            "month": row.month,

            "avg_temperature":
                row.avg_temperature,

            "rainfall":
                row.rainfall,

            "humidity":
                row.humidity
        })

    return data