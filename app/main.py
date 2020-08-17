"""
Main app entry poitn.
"""

from fastapi import FastAPI

from app.api.v1 import api_router

app = FastAPI()


@app.get("/")
def read_root():
    """
    Exampler endpoint
    """
    return {"Hello": "World"}


# Routers
app.include_router(api_router)
