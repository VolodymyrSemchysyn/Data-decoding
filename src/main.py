from fastapi import FastAPI

from routes import movie_router

app = FastAPI(
    title="Data-decoding",
    description="App for decoding and encoding data",
)

api_version_prefix = "/api"

app.include_router(data_router, prefix=f"{api_version_prefix}/data", tags=["data"])