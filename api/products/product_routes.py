from fastapi import APIRouter, Depends
from api.products.create_products import create_products
from api.products.delete_product import deactivate_product
from api.products.get_product_by_id import get_products_by_id
from api.products.get_products import get_products
from api.products.update_product import update_product
from auth.auth_utils import get_current_user

from schemas.schemas import (
    ProductUpdate,
    ProductResponse,
    ProductCreate
)

product_router =APIRouter(
    prefix = "/products",
    tags = ["Products"]
)

@product_router.post(
    "/create",
    response_model=ProductResponse
)
def createProduct(product: ProductCreate, current_user: dict = Depends(get_current_user)):
    return create_products(product)


@product_router.get(
    "/getall",
    response_model=list[ProductResponse]
)
def getAllProducts():
    return get_products()


@product_router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def getProductById(product_id: str):
    return get_products_by_id(product_id)


@product_router.put(
    "/update/{product_id}"
)
def updateProduct(product_id: str, product: ProductUpdate, current_user: dict = Depends(get_current_user)):
    return update_product(product_id, product)


@product_router.delete(
    "/delete/{product_id}"
)
def deactivateProduct(product_id: str, current_user: dict = Depends(get_current_user)):
    return deactivate_product(product_id)
