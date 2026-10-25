from fastapi import APIRouter, Depends
from typing import List

from schemas.schemas import SaleResponse, SaleCreate, SaleUpdate
from api.sales.get_sales import get_sales
from api.sales.get_sale import get_sale
from api.sales.create_sale import create_sale
from api.sales.update_sale import update_sale
from api.sales.delete_sale import delete_sale
from auth.auth_utils import get_current_user

router = APIRouter(prefix="/api/sales", tags=["Sales"])


@router.get("/", response_model=List[SaleResponse])
def read_all_sales():
    return get_sales()


@router.get("/{sale_id}", response_model=SaleResponse)
def read_sale(sale_id: str):
    return get_sale(sale_id)


@router.post("/", response_model=SaleResponse)
def add_sale(sale_data: SaleCreate, current_user: dict = Depends(get_current_user)):
    return create_sale(sale_data)


@router.put("/{sale_id}", response_model=SaleResponse)
def edit_sale(sale_id: str, sale_data: SaleUpdate, current_user: dict = Depends(get_current_user)):
    return update_sale(sale_id, sale_data)


@router.delete("/{sale_id}")
def remove_sale(sale_id: str, current_user: dict = Depends(get_current_user)):
    return delete_sale(sale_id)
