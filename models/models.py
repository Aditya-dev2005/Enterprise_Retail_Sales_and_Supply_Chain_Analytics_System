from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Date, DateTime, Integer, Float, ForeignKey

Base = declarative_base()


class Products(Base):
    __tablename__ = "products"

    product_id = Column(String(30), primary_key=True)
    product_name = Column(String(100), nullable=False)
    category = Column(String(30), nullable=False)
    brand = Column(String(100), nullable=False)
    unit_price = Column(Float, nullable=False)
    supplier_id = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)

    sales = relationship(
        "Sales", back_populates="product", cascade="all, delete-orphan"
    )
    inventory = relationship(
        "Inventory", back_populates="product", cascade="all, delete-orphan"
    )


class Stores(Base):
    __tablename__ = "stores"

    store_id = Column(String(30), primary_key=True)
    store_name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    store_manager = Column(String(100), nullable=False)
    opening_date = Column(Date, nullable=False)
    status = Column(String(100), nullable=False)

    sales = relationship("Sales", back_populates="store", cascade="all, delete-orphan")
    inventory = relationship(
        "Inventory", back_populates="store", cascade="all, delete-orphan"
    )


class Customers(Base):
    __tablename__ = "customers"

    customer_id = Column(String(30), primary_key=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    mobile = Column(String(20), nullable=False)
    city = Column(String(100), nullable=False)
    registration_date = Column(Date, nullable=False)
    customer_type = Column(String(30), nullable=False)

    sales = relationship(
        "Sales", back_populates="customer", cascade="all, delete-orphan"
    )


class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(String(30), primary_key=True)
    product_id = Column(String(30), ForeignKey("products.product_id"), nullable=False)
    store_id = Column(String(30), ForeignKey("stores.store_id"), nullable=False)
    customer_id = Column(
        String(30), ForeignKey("customers.customer_id"), nullable=False
    )
    quantity = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    payment_mode = Column(String(30), nullable=False)

    product = relationship("Products", back_populates="sales")
    store = relationship("Stores", back_populates="sales")
    customer = relationship("Customers", back_populates="sales")


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(String(30), primary_key=True)
    product_id = Column(String(30), ForeignKey("products.product_id"), nullable=False)
    store_id = Column(String(30), ForeignKey("stores.store_id"), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    reorder_level = Column(Integer, nullable=False)
    last_updated = Column(Date, nullable=False)

    product = relationship("Products", back_populates="inventory")
    store = relationship("Stores", back_populates="inventory")


class RejectedRecord(Base):
    __tablename__ = "rejected_records"

    rejected_id = Column(Integer, primary_key=True, autoincrement=True)
    table_name = Column(String(50), nullable=False)
    record_data = Column(String(5000), nullable=False)
    reason = Column(String(500), nullable=False)
    rejected_date = Column(Date, nullable=False)


class PipelineExecution(Base):
    __tablename__ = "pipeline_execution"

    execution_id = Column(Integer, primary_key=True, autoincrement=True)
    pipeline_name = Column(String(100), nullable=False)
    start_time = Column(Date, nullable=False)
    end_time = Column(Date, nullable=False)
    status = Column(String(30), nullable=False)
    records_processed = Column(Integer, nullable=False)
    records_failed = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    created_at = Column(DateTime, nullable=False)
