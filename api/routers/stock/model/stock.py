

from typing import List

from pydantic import BaseModel, ValidationError, validator


class StockPrice(BaseModel):
    market: str
    symbol: str
    alias: str
    price: float
    currency: str
    updated_time: str


class StockPrices(BaseModel):
    prices: List[StockPrice] = []


class Ticker(BaseModel):
    market: str
    symbol: str


class Tickers(BaseModel):
    tickers: List[Ticker]

    @validator('tickers')
    def check_tickers(cls, v):
        if len(v) == 0:
            raise ValueError('tickers cannot be empty')
        return v
