import os
from time import sleep
from enum import Enum

import httpx
from pydantic import BaseModel
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
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
    reason: str | None = None

    class Meta:
        database = redis
        use_enum_values = True


class OrderRequest(BaseModel):
    product_id: str
    quantity: int


def order_completed(order: Order) -> None:
    sleep(5)  # Payment confirmation or not.
    order.status = OrderStatus.COMPLETED
    order.save()

    # Send event order through RedisStreams to update product
    # without sending it through REST API.
    redis.xadd("order_completed", order.dict(), "*")


@app.get(
    "/api/orders",
    summary="Get all orders",
    tags=["Orders"],
)
async def get_orders():
    return [Order.get(order_pk) for order_pk in Order.all_pks()]


@app.get(
    "/api/orders/{order_pk}",
    summary="Get an order based on his pk",
    tags=["Orders"],
)
async def get_order(order_pk: str):
    try:
        return Order.get(order_pk)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with pk {order_pk} was not found",
        )


@app.post(
    "/api/orders",
    summary="Create an order",
    tags=["Orders"],
    status_code=status.HTTP_201_CREATED,
)
async def create_order(
    background_tasks: BackgroundTasks,
    order: OrderRequest
):
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(
                f"{os.getenv('INVENTORY_API_URL')}/api/products/{order.product_id}"
            )
            r.raise_for_status()
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

    background_tasks.add_task(order_completed, order)

    return order
