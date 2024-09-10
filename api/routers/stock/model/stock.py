

from typing import List, Self

from pydantic import BaseModel, ValidationError, validator

from src.enum.available_markets import AvailableMarkets


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

    @validator('market')
    def check_market(cls, v):
        if AvailableMarkets(v).value == AvailableMarkets.UNKNOWN:
            raise ValueError(f"market {v} not found")
        return v

    def __lt__(self, other: Self):
        if self.market != other.market:
            return self.market < other.market
        return self.symbol < other.symbol

    def __gt__(self, other: Self):
        if self.market != other.market:
            return self.market > other.market
        return self.symbol > other.symbol


class Tickers(BaseModel):
    tickers: List[Ticker]

    @validator('tickers')
    def check_tickers(cls, v):
        if len(v) == 0:
            raise ValueError('tickers cannot be empty')
        return v
