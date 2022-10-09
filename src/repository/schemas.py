from pydantic import BaseModel


class Ticker(BaseModel):
    id: int
    name: str


class TickerWithValues(Ticker):
    values: list[int]
