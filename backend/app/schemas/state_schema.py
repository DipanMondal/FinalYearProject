from pydantic import BaseModel


class StateStatusResponse(BaseModel):
    state: str

    ingested: bool
    trained: bool
    analysed: bool