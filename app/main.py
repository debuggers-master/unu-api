"""
Main app entry poitn.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """
    Exampler endpoint
    """
    return {"Hello": "World"}
