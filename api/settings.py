from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.healthcheck import healthcheck

tags = [
    {
        'name': 'Utilities',
        'description': 'Backend Utilities API'
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
