from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.healthcheck import healthcheck
from api.routers.symbol_list import symbol_list
from api.routers.stock import stock
from api.routers.forex_rate import forex_rate
from api.routers.profile import profile

tags = [
    {
        'name': 'Utilities',
        'description': 'Backend Utilities API'
    },
    {
        'name': 'Symbols',
        'description': 'Available Symbols API'
    },
    {
        'name': 'Stcok',
        'description': 'Stcok Info API'
    },
    {
        'name': 'Forex',
        'description': 'Forex Exchange Rate API'
    },
    {
        'name': 'Profile',
        'description': 'User Profile API'
    },
]


origins = ["*"]
app = FastAPI(title="Niffler Backend API",
              openapi_tags=tags,
              version="0.1.0",
              docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck.router,
                   prefix="/api", tags=["Utilities"])
app.include_router(symbol_list.router,
                   prefix="/api/symbols", tags=["Symbols"])
app.include_router(stock.router,
                   prefix="/api/stock", tags=["Stcok"])

app.include_router(forex_rate.router,
                   prefix="/api/forex", tags=["Forex"])

app.include_router(profile.router,
                   prefix="/api/profile", tags=["Profile"])
