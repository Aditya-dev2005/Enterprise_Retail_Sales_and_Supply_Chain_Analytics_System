from fastapi import APIRouter, Depends, status

from schemas.schemas import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

from api.customers.create_customer import create_customer
from api.customers.get_customers import get_all_customers
from api.customers.get_customer_by_id import get_customer_by_id
from api.customers.update_customer import update_customer
from typing import List
from api.customers.delete_customer import delete_customer
from auth.auth_utils import get_current_user


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_customer(customer: CustomerCreate, current_user: dict = Depends(get_current_user)):
    return create_customer(customer)


@router.get(
    "",
    response_model=List[CustomerResponse],
)
def get_customers():
    return get_all_customers()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(customer_id: str):
    return get_customer_by_id(customer_id)


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def modify_customer(
    customer_id: str,
    customer: CustomerUpdate,
    current_user: dict = Depends(get_current_user),
):
    return update_customer(customer_id, customer)


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_200_OK,
)
def remove_customer(customer_id: str, current_user: dict = Depends(get_current_user)):
    return delete_customer(customer_id)
