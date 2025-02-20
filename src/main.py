from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routes.data import router

app = FastAPI(
    title="Data-decoding",
    description="App for decoding and encoding data",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_version_prefix = "/api"

app.include_router(router, prefix=f"{api_version_prefix}/data", tags=["data"])