from fastapi import FastAPI

from app.core.config import settings
from app.database import init_db

from app.api.routes.health import router as health_router
from app.api.routes.states import router as states_router


init_db()

app = FastAPI(
    title=settings.APP_NAME
)

app.include_router(health_router)
app.include_router(states_router)

@app.get("/")
def root():
    return {
        "message": "Climate Intelligence Platform API"
    }