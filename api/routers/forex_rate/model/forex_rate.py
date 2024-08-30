
from typing import List

from pydantic import BaseModel


class ForexRate(BaseModel):
    base: str = "USD"
    quote: str
    rate: float
    updated_time: str


class ForexRates(BaseModel):
    rates: List[ForexRate] = []


class ForexAvaliableSymbols(BaseModel):
    symbols: List[str] = []


class ForexRateRequest(BaseModel):
    base: str = "USD"
    quote: List[str]
