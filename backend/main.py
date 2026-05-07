from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.database import init_db

from app.api.routes.health import router as health_router
from app.api.routes.states import router as states_router
from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.features import router as feature_router
from app.api.routes.training import router as training_router
from app.api.routes.forecast import router as forecast_router
from app.api.routes.analysis import router as analysis_router



from app.core.exceptions import StateNotFoundException


init_db()

app = FastAPI(
    title=settings.APP_NAME
)


@app.exception_handler(StateNotFoundException)
async def state_not_found_handler(
    request,
    exc: StateNotFoundException
):

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": f"State '{exc.state}' not found"
        }
    )


app.include_router(health_router)
app.include_router(states_router)
app.include_router(ingestion_router)
app.include_router(feature_router)
app.include_router(training_router)
app.include_router(forecast_router)
app.include_router(analysis_router)


@app.get("/")
def root():

    return {
        "message": "Climate Intelligence Platform API"
    }