from sqlalchemy import select

from database.database_connection import sessionLocal
from models.models import Customers
from schemas.schemas import CustomerCreate
from logger_config import logger
from fastapi import HTTPException


def create_customer(customer: CustomerCreate):
    session = sessionLocal()

    try:
        stmt = select(Customers).where(Customers.customer_id == customer.customer_id)

        existing_customer = session.scalar(stmt)

        if existing_customer:
            logger.error(f"CustomerAlreadyExists {customer.customer_id}")
            raise HTTPException(status_code=404, detail="Customer not found")

        new_customer = Customers(
            customer_id=customer.customer_id,
            customer_name=customer.customer_name,
            email=customer.email,
            mobile=customer.mobile,
            city=customer.city,
            registration_date=customer.registration_date,
            customer_type=customer.customer_type,
        )

        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)

        logger.info(f"Customer {new_customer.customer_id} created successfully")

        return new_customer

    except Exception as e:
        session.rollback()
        logger.error("Failed to create customer", e)
        raise e

    finally:
        session.close()
