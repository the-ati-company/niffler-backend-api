
from enum import Enum


class AvailableMarkets(Enum):
    CRYPTO = "CRYPTO"
    TWSE = "TWSE"
    TPEX = "TPEX"
    AMEX = "AMEX"
    NASDAQ = "NASDAQ"
    NYSE = "NYSE"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: str):
        value = value.upper()
        if value in [market.value for market in cls]:
            return cls(value)
        return cls.UNKNOWN
