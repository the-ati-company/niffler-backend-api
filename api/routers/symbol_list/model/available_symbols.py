
from typing import List

from pydantic import BaseModel


class AvailableSymbols(BaseModel):
    market: str
    symbols: List[str]


class AvailableSymbolsResponse(BaseModel):
    data: List[AvailableSymbols]
