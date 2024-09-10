
from typing import List, Optional

from pydantic import BaseModel, ValidationError, validator

from api.routers.stock.model.stock import Ticker

from src.enum.available_os import AvailableOS


def sequence_arranger(v, sort_field="alias"):
    need_rearrange_sequence = False
    for i, item in enumerate(v):
        if not item.sequence:
            need_rearrange_sequence = True
            break
    if need_rearrange_sequence:
        # sort by field, default alias
        v = sorted(v, key=lambda x: x.__getattribute__(sort_field))
        for i, item in enumerate(v):
            item.sequence = i
    return v


class Holding(BaseModel):
    ticker: Ticker
    quantity: float
    sequence: Optional[int] = None


class HoldingGroup(BaseModel):
    alias: str = ""
    holdings: Optional[List[Holding]] = []
    sequence: Optional[int] = None

    @validator('holdings')
    def check_holdings_sequence(cls, v):
        v = sequence_arranger(v, "ticker")
        return v


class Portfolio(BaseModel):
    alias: str = ""
    holding_groups: Optional[List[HoldingGroup]] = []
    sequence: Optional[int] = None

    @validator('holding_groups')
    def check_holding_groups_sequence(cls, v):
        v = sequence_arranger(v)
        return v


class Profile(BaseModel):
    device_uid: str
    os: AvailableOS
    user_name: str = ""
    email: str = ""
    phone: str = ""
    primary_currency: str = "USD"
    secondary_currency: str = "TWD"
    portfolios: List[Portfolio] = []

    @validator('portfolios')
    def check_portfolio_sequence(cls, v):
        v = sequence_arranger(v)
        return v
