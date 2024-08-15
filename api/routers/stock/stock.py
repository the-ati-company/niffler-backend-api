
import json

from fastapi import Path
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.handler.firestore_handler import FirestoreHandler
from src.enum.available_markets import AvailableMarkets

from api.routers.stock.model.stock import StockPrice

router = APIRouter()

firestore_handler = FirestoreHandler()


@router.get("/price/{market}/{ticker}", status_code=200, response_model=StockPrice)
async def get_stock_price(market: str, ticker: str):
    if AvailableMarkets(market) == AvailableMarkets.UNKNOWN:
        return JSONResponse(content={"message": f"market {market} not found"}, status_code=400)
    market = AvailableMarkets(market)
    all_stocks = {}
    stock_price_docs = firestore_handler.get_colletion(
        market.value).get()

    for doc in stock_price_docs:
        stocks = json.loads(doc.to_dict()['symbols'])
        all_stocks.update(stocks)

    ticker_key = f"{ticker}@{market.value}"
    if ticker_key not in all_stocks:
        return JSONResponse(content={"message": f"ticker {ticker} not found in {market.value}"}, status_code=400)

    stock = all_stocks[ticker_key]
    stock_price = StockPrice(market=stock['market'],
                             symbol=stock['symbol'],
                             alias=stock['alias'],
                             price=stock['price'],
                             currency=stock['currency'],
                             updated_time=stock['updated'])

    return stock_price
