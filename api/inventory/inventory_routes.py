from typing import List
from fastapi import APIRouter

from schemas.schemas import InventoryResponse
from api.inventory import inventory_operations 

inventory_router = APIRouter(
    prefix="/api/inventory",
    tags=["Inventory"]
)


@inventory_router.get("", response_model=List[InventoryResponse])
def get_inventory():
    return inventory_operations.get_all_inventory()


@inventory_router.get("/store/{store_id}", response_model=List[InventoryResponse])
def get_store_inventory(store_id: str):
    return inventory_operations.get_inventory_by_store(store_id)


@inventory_router.get("/low-stock", response_model=List[InventoryResponse])
def get_low_stock_inventory():
    return inventory_operations.get_low_stock_inventory()