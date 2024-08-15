from fastapi import APIRouter

from src.handler.firestore_handler import FirestoreHandler

from api.routers.symbol_list.model.available_symbols import AvailableSymbols, AvailableSymbolsResponse

router = APIRouter()

firestore_handler = FirestoreHandler()


@router.get("/symbol-list", status_code=200, response_model=AvailableSymbolsResponse)
async def available_symbol_list():
    available_symbol_docs = firestore_handler.get_colletion(
        "available_symbols").get()
    data = []
    for doc in available_symbol_docs:
        available_symbols = AvailableSymbols(market=doc.id,
                                             symbols=doc.to_dict()['symbols'])
        data.append(available_symbols)
    return AvailableSymbolsResponse(data=data)
