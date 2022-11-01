import os
from typing import Any

from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI, HTTPException, status, Response
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

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


class Product(HashModel):
    name: str
    price: float
    quantity_available: int

    class Meta:
        database = redis


def format_output(pk: str) -> dict[str, Any]:
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity_available": product.quantity_available,
    }


@app.get(
    "/api/products",
    summary="Get all products",
    tags=["Products"],
)
async def get_products():
    return [format_output(pk) for pk in Product.all_pks()]


@app.get(
    "/api/products/{product_pk}",
    summary="Get a product based on his pk",
    tags=["Products"],
)
async def get_product(pk: str):
    try:
        return Product.get(pk)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with pk {pk} was not found",
        )


@app.post(
    "/api/products",
    summary="Creates a new product",
    tags=["Products"],
)
async def create_product(product: Product):
    return product.save()


@app.delete(
    "/api/products/{product_pk}",
    summary="Delete a product based on his pk",
    tags=["Products"],
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_product(pk: str):
    deleted = Product.delete(pk)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with pk {pk} was not found",
        )
