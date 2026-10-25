from typing import List

from fastapi import APIRouter, Depends, status

from schemas.schemas import StoreCreate, StoreUpdate, StoreResponse

from api.stores.get_stores import get_all_stores
from api.stores.get_store_by_id import get_store_by_id
from api.stores.create_store import create_store
from api.stores.update_store import update_store
from auth.auth_utils import get_current_user


router = APIRouter(prefix="/stores", tags=["Stores"])


@router.get("", response_model=List[StoreResponse], status_code=status.HTTP_200_OK)
def get_stores():
    return get_all_stores()


@router.get("/{store_id}", response_model=StoreResponse, status_code=status.HTTP_200_OK)
def get_store(store_id: str):
    return get_store_by_id(store_id)


@router.post("", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
def add_store(store: StoreCreate, current_user: dict = Depends(get_current_user)):
    return create_store(store)


@router.put("/{store_id}", response_model=StoreResponse, status_code=status.HTTP_200_OK)
def modify_store(store_id: str, store: StoreUpdate, current_user: dict = Depends(get_current_user)):
    return update_store(store_id, store)
