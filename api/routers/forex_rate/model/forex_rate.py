
from typing import List

from pydantic import BaseModel


class ForexRate(BaseModel):
    base: str = "USD"
    quote: str
    rate: float
    updated_time: str


class ForexRates(BaseModel):
    rates: List[ForexRate] = []


class ForexRateRequest(BaseModel):
    base: str = "USD"
    quote: List[str]
