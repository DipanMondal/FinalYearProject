from pydantic import BaseModel


class IngestionRequest(BaseModel):

    state: str

    start_year: int

    end_year: int