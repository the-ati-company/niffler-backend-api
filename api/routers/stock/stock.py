
import json

from typing import List, Dict, Any
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.handler.firestore_handler import FirestoreHandler
from src.enum.available_markets import AvailableMarkets

from api.routers.stock.model.stock import StockPrice, StockPrices, Ticker, Tickers

router = APIRouter()

firestore_handler = FirestoreHandler()


def get_stocks_by_market(market: str) -> Dict[str, Any]:
    all_stocks = {}
    market = AvailableMarkets(market)
    if market == AvailableMarkets.UNKNOWN:
        return all_stocks
    stock_price_docs = firestore_handler.get_colletion(
        market.value).get()

    for doc in stock_price_docs:
        stocks = json.loads(doc.to_dict()['symbols'])
        all_stocks.update(stocks)
    return all_stocks


def get_stocks_in_market(stocks: Dict[str, Any], ticker_keys: str) -> StockPrices:
    stock_prices = []
    for ticker_key in ticker_keys:
        if ticker_key in stocks:
            stock = stocks[ticker_key]
            stock_price = StockPrice(market=stock['market'],
                                     symbol=stock['symbol'],
                                     alias=stock['alias'],
                                     price=stock['price'],
                                     currency=stock['currency'],
                                     updated_time=stock['updated'])
            stock_prices.append(stock_price)
    return StockPrices(prices=stock_prices)


@router.get("/price/{market}/{ticker}", status_code=200, response_model=StockPrices)
async def get_stock_price(market: str, ticker: str):
    if AvailableMarkets(market) == AvailableMarkets.UNKNOWN:
        return JSONResponse(content={"message": f"market {market} not found"}, status_code=400)
    market = AvailableMarkets(market)
    ticker_key = f"{ticker}@{market.value}"

    all_stocks = get_stocks_by_market(market.value)

    if ticker_key not in all_stocks:
        return JSONResponse(content={"message": f"ticker {ticker} not found in {market.value}"}, status_code=400)

    return get_stocks_in_market(all_stocks, [ticker_key])


@router.post("/price/tickers", status_code=200, response_model=StockPrices)
async def get_stock_prices(tickers: Tickers):
    if len(tickers.tickers) == 0:
        return JSONResponse(content={"message": "tickers cannot be empty"}, status_code=400)

    tickers_by_market = {}
    for ticker in tickers.tickers:
        market = AvailableMarkets(ticker.market)
        if market == AvailableMarkets.UNKNOWN:
            return JSONResponse(content={"message": f"market {ticker.market} not found"}, status_code=400)
        ticker_key = f"{ticker.symbol}@{market.value}"
        if market not in tickers_by_market:
            tickers_by_market[market] = []
        tickers_by_market[market].append(ticker_key)

    all_stock_prices = StockPrices()

    for market, ticker_keys in tickers_by_market.items():
        all_stocks = get_stocks_by_market(market.value)
        stock_prices = get_stocks_in_market(all_stocks, ticker_keys)
        all_stock_prices.prices.extend(stock_prices.prices)

    return all_stock_prices
