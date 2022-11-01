import os
from typing import Union

from redis_om import get_redis_connection
from fastapi import FastAPI

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
redis_conn = get_redis_connection()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
