

from typing import List

from pydantic import BaseModel, ValidationError, validator


class StockPrice(BaseModel):
    market: str
    symbol: str
    alias: str
    price: float
    currency: str
    updated_time: str
