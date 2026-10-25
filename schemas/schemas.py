from datetime import date
from pydantic import BaseModel, ConfigDict


# -------------------- Products --------------------

class ProductCreate(BaseModel):
    product_name: str
    category: str
    brand: str
    unit_price: float
    supplier_id: str
    status: str


class ProductUpdate(BaseModel):
    product_name: str
    category: str
    brand: str
    unit_price: float
    supplier_id: str
    status: str


class ProductResponse(ProductCreate):
    model_config = ConfigDict(from_attributes=True)


# -------------------- Stores --------------------

class StoreCreate(BaseModel):
    store_id: str
    store_name: str
    city: str
    state: str
    store_manager: str
    opening_date: date
    status: str


class StoreUpdate(BaseModel):
    store_name: str
    city: str
    state: str
    store_manager: str
    opening_date: date
    status: str


class StoreResponse(StoreCreate):
    model_config = ConfigDict(from_attributes=True)


# -------------------- Customers --------------------

class CustomerCreate(BaseModel):
    customer_id: str
    customer_name: str
    email: str
    mobile: str
    city: str
    registration_date: date
    customer_type: str


class CustomerUpdate(BaseModel):
    customer_name: str
    email: str
    mobile: str
    city: str
    registration_date: date
    customer_type: str


class CustomerResponse(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)


# -------------------- Sales --------------------

class SaleCreate(BaseModel):
    sale_id: str
    product_id: str
    store_id: str
    customer_id: str
    quantity: int
    sale_date: date
    discount_percentage: float
    payment_mode: str


class SaleUpdate(BaseModel):
    product_id: str
    store_id: str
    customer_id: str
    quantity: int
    sale_date: date
    discount_percentage: float
    payment_mode: str


class SaleResponse(SaleCreate):
    model_config = ConfigDict(from_attributes=True)


# -------------------- Inventory --------------------

class InventoryCreate(BaseModel):
    inventory_id: str
    product_id: str
    store_id: str
    available_quantity: int
    reorder_level: int
    last_updated: date


class InventoryUpdate(BaseModel):
    product_id: str
    store_id: str
    available_quantity: int
    reorder_level: int
    last_updated: date


class InventoryResponse(InventoryCreate):
    model_config = ConfigDict(from_attributes=True)