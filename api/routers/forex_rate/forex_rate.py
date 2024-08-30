

import requests

from typing import List


from fastapi import APIRouter
from fastapi.responses import JSONResponse


from api.routers.forex_rate.model.forex_rate import ForexRate, ForexRates, ForexRateRequest, ForexAvaliableSymbols

router = APIRouter()


def get_forex_available_symbols() -> ForexAvaliableSymbols:
    r = requests.get('https://tw.rter.info/capi.php')
    all_rates = r.json()
    all_currencies = list(all_rates.keys())
    all_symbols = set()
    all_symbols.add("USD")

    for forex_rate in all_currencies:
        symbol = forex_rate.replace("USD", "")
        if symbol and symbol != "USD" and symbol != "":
            all_symbols.add(symbol)
    all_symbols = list(all_symbols)

    return ForexAvaliableSymbols(symbols=all_symbols)


def get_forex_rate(pairs: ForexRateRequest) -> ForexRates:
    r = requests.get('https://tw.rter.info/capi.php')
    all_rates = r.json()
    forex_rates = ForexRates()

    base_currency = pairs.base

    for q_c in pairs.quote:
        pair = f"{base_currency}{q_c}"
        if pair in all_rates or q_c in all_rates:
            quote_key = pair if pair in all_rates else q_c
            rate = all_rates[quote_key]['Exrate']
            updated_time = all_rates[quote_key]['UTC']
            forex_rate = ForexRate(
                base=base_currency,
                quote=q_c,
                rate=rate,
                updated_time=updated_time)
            forex_rates.rates.append(forex_rate)
    return forex_rates


@router.get("/symbol-list", status_code=200, response_model=ForexAvaliableSymbols)
async def forex_available_symbols():
    return get_forex_available_symbols()


@router.post("/rate", status_code=200, response_model=ForexRates)
async def forex_rate(forex_rate_request: ForexRateRequest):
    return get_forex_rate(forex_rate_request)
