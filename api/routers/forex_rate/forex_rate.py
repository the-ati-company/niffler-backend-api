

import requests

from typing import List


from fastapi import APIRouter
from fastapi.responses import JSONResponse


from api.routers.forex_rate.model.forex_rate import ForexRate, ForexRates, ForexRateRequest

router = APIRouter()


def get_forex_rate(pairs: ForexRateRequest) -> ForexRates:
    r = requests.get('https://tw.rter.info/capi.php')
    all_rates = r.json()
    forex_rates = ForexRates()

    base_currency = pairs.base

    for q_c in pairs.quote:
        pair = f"{base_currency}{q_c}"
        if pair in all_rates:
            rate = all_rates[pair]['Exrate']
            updated_time = all_rates[pair]['UTC']
            forex_rate = ForexRate(
                base=base_currency,
                quote=q_c,
                rate=rate,
                updated_time=updated_time)
            forex_rates.rates.append(forex_rate)
    return forex_rates


@router.post("/rate", status_code=200, response_model=ForexRates)
async def forex_rate(forex_rate_request: ForexRateRequest):
    return get_forex_rate(forex_rate_request)
