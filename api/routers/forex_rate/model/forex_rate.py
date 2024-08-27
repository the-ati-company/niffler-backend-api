
from typing import List

from pydantic import BaseModel


class ForexRate(BaseModel):
    base_currency: str = "USD"
    quote_currency: str
    rate: float
    updated_time: str


class ForexRates(BaseModel):
    rates: List[ForexRate] = []


class ForexRateRequest(BaseModel):
    base_currency: str = "USD"
    quote_currencies: List[str]
