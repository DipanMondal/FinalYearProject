from pathlib import Path

import joblib

from app.core.config import settings


def save_model(
    model,
    state: str,
    variable: str
):

    model_dir = (
        Path(settings.MODELS_DIR)
        / state
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    model_path = (
        model_dir
        / f"{variable}_sarimax.pkl"
    )

    joblib.dump(model, model_path)

    return str(model_path)


def load_model(
    model_path: str
):

    return joblib.load(model_path)