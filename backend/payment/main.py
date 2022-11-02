import os
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI, HTTPException, status, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Different database.
redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: OrderStatus

    class Meta:
        database = redis
        use_enum_values = True


class OrderRequest(BaseModel):
    product_id: str
    quantity: int


@app.post(
    "/api/orders",
    summary="Create an order",
    tags=["Orders"],
    status_code=status.HTTP_201_CREATED,
)
async def create_order(order: OrderRequest):
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"{os.getenv('INVENTORY_API_URL')}/api/products/{order.product_id}"
            )
        except httpx.HTTPError as err:
            raise HTTPException(
                status_code=err.response.status_code,
                detail=f"Error getting product {order.product_id}",
            )
    
    product = r.json()
    order = Order(
        product_id=order.product_id,
        price=product["price"],
        fee=product["price"] * 0.2,
        total=product["price"] * 1.2,
        quantity=order.quantity,
        status=OrderStatus.PENDING,
    )
    order.save()

    return order
