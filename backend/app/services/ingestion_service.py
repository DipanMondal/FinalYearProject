from sqlalchemy.orm import Session

from app.models.metadata import Metadata
from app.models.climate_data import ClimateData

from app.services.nasa_power_service import (
    fetch_climate_data
)

from app.utils.state_coordinates import (
    STATE_COORDINATES
)

from app.utils.climate_parser import (
    parse_climate_data
)

from app.services.pipeline_logger_service import (
    log_pipeline_event
)

from app.services.state_status_service import (
    create_or_update_state_status
)


def ingest_state_climate_data(
    db: Session,
    state: str,
    start_year: int,
    end_year: int
):

    if state not in STATE_COORDINATES:

        raise ValueError(
            f"Coordinates not found for state '{state}'"
        )

    coords = STATE_COORDINATES[state]

    raw_data = fetch_climate_data(
        latitude=coords["lat"],
        longitude=coords["lon"],
        start_year=start_year,
        end_year=end_year
    )

    parsed_rows = parse_climate_data(
        state=state,
        raw_data=raw_data
    )

    for row in parsed_rows:

        climate_row = ClimateData(**row)

        db.add(climate_row)

    metadata = Metadata(
        state=state,
        latitude=coords["lat"],
        longitude=coords["lon"],
        source="NASA POWER API",
        start_year=start_year,
        end_year=end_year,
        records_count=len(parsed_rows)
    )

    db.add(metadata)

    create_or_update_state_status(
        db=db,
        state=state,
        ingested=True
    )

    log_pipeline_event(
        db=db,
        state=state,
        pipeline="INGESTION",
        status="SUCCESS",
        message="Climate data ingested successfully"
    )

    db.commit()

    return {
        "state": state,
        "records_ingested": len(parsed_rows)
    }