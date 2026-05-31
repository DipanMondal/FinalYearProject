import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy.orm import Session

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.ai_prompt import AI_CLIMATE_INSIGHT_PROMPT
from app.core.config import settings
from app.models.climate_data import ClimateData
from app.services.pipeline_logger_service import log_pipeline_event


AI_INSIGHT_FILENAME = "ai_insight_report.json"


def load_raw_climate_dataframe(
    db: Session,
    state: str
) -> pd.DataFrame:

    rows = (
        db.query(ClimateData)
        .filter(ClimateData.state == state)
        .order_by(ClimateData.year, ClimateData.month)
        .all()
    )

    data = []

    for row in rows:
        data.append({
            "state": row.state,
            "year": row.year,
            "month": row.month,
            "avg_temperature": row.avg_temperature,
            "rainfall": row.rainfall,
            "humidity": row.humidity,
        })

    return pd.DataFrame(data)


def dataframe_to_prompt_dataset(df: pd.DataFrame) -> str:
    """
    Convert raw climate dataframe into compact CSV text.
    CSV is easier for the LLM to read than JSON and uses fewer tokens.
    """

    clean_df = df.copy()

    numeric_columns = [
        "avg_temperature",
        "rainfall",
        "humidity",
    ]

    for column in numeric_columns:
        if column in clean_df.columns:
            clean_df[column] = clean_df[column].round(3)

    return clean_df.to_csv(index=False)


def extract_llm_text(response: Any) -> str:
    """
    Supports both older Gemini responses where response.content is a string
    and newer LangChain responses where response.text is the safest accessor.
    """

    response_text = getattr(response, "text", None)

    if isinstance(response_text, str) and response_text.strip():
        return response_text

    content = getattr(response, "content", "")

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = []

        for block in content:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(str(block["text"]))
            else:
                text_parts.append(str(block))

        return "\n".join(text_parts)

    return str(content)


def build_ai_prompt(
    state: str,
    dataset: str,
    forecast_horizon: int = 12
) -> str:

    return (
        AI_CLIMATE_INSIGHT_PROMPT
        .replace("{state}", state)
        .replace("{forecast_horizon}", str(forecast_horizon))
        .replace("{dataset}", dataset)
    )


def get_ai_insight_path(state: str) -> Path:

    return (
        Path(settings.ARTIFACTS_DIR)
        / state
        / AI_INSIGHT_FILENAME
    )


def save_ai_insight_report(
    state: str,
    payload: dict
) -> Path:

    artifact_dir = (
        Path(settings.ARTIFACTS_DIR)
        / state
    )

    artifact_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = artifact_dir / AI_INSIGHT_FILENAME

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(
            payload,
            f,
            indent=4,
            ensure_ascii=False
        )

    return report_path


def generate_ai_insight_report(
    db: Session,
    state: str,
    forecast_horizon: int = 12
) -> dict:
    """
    AI insight unit called from the existing statistical analysis pipeline.
    It reads raw climate_data, sends it to Gemini through LangChain,
    and stores a separate AI insight artifact.
    """

    df = load_raw_climate_dataframe(
        db=db,
        state=state
    )

    generated_at = datetime.utcnow().isoformat()

    if df.empty:
        payload = {
            "success": False,
            "state": state,
            "generated_at": generated_at,
            "model": None,
            "report_markdown": "",
            "error": f"No raw climate data found for {state}.",
        }

        save_ai_insight_report(
            state=state,
            payload=payload
        )

        return payload

    if not settings.GOOGLE_API_KEY:
        payload = {
            "success": False,
            "state": state,
            "generated_at": generated_at,
            "model": settings.GEMINI_MODEL,
            "report_markdown": "",
            "rows_used": int(len(df)),
            "error": "GOOGLE_API_KEY is missing in backend .env file.",
        }

        save_ai_insight_report(
            state=state,
            payload=payload
        )

        log_pipeline_event(
            db=db,
            state=state,
            pipeline="AI_ANALYSIS",
            status="FAILED",
            message="GOOGLE_API_KEY missing"
        )

        return payload

    dataset = dataframe_to_prompt_dataset(df)

    prompt = build_ai_prompt(
        state=state,
        dataset=dataset,
        forecast_horizon=forecast_horizon
    )

    try:
        llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            api_key=settings.GOOGLE_API_KEY,
            temperature=settings.GEMINI_TEMPERATURE,
            max_retries=2,
        )

        response = llm.invoke(prompt)

        report_markdown = extract_llm_text(response)

        payload = {
            "success": True,
            "state": state,
            "generated_at": generated_at,
            "model": settings.GEMINI_MODEL,
            "forecast_horizon": forecast_horizon,
            "rows_used": int(len(df)),
            "year_range": {
                "start_year": int(df["year"].min()),
                "end_year": int(df["year"].max()),
            },
            "report_markdown": report_markdown,
            "error": None,
        }

        report_path = save_ai_insight_report(
            state=state,
            payload=payload
        )

        payload["report_path"] = str(report_path)

        log_pipeline_event(
            db=db,
            state=state,
            pipeline="AI_ANALYSIS",
            status="SUCCESS",
            message="AI insight report generated"
        )

        return payload

    except Exception as exc:
        payload = {
            "success": False,
            "state": state,
            "generated_at": generated_at,
            "model": settings.GEMINI_MODEL,
            "forecast_horizon": forecast_horizon,
            "rows_used": int(len(df)),
            "report_markdown": "",
            "error": str(exc),
        }

        save_ai_insight_report(
            state=state,
            payload=payload
        )

        log_pipeline_event(
            db=db,
            state=state,
            pipeline="AI_ANALYSIS",
            status="FAILED",
            message=str(exc)[:500]
        )

        return payload