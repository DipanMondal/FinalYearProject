from sqlalchemy.orm import Session

from app.models.pipeline_log import PipelineLog


def log_pipeline_event(
    db: Session,
    state: str,
    pipeline: str,
    status: str,
    message: str
):

    log = PipelineLog(
        state=state,
        pipeline=pipeline,
        status=status,
        message=message
    )

    db.add(log)

    db.commit()