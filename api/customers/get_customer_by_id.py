from sqlalchemy import select
from fastapi import HTTPException
from database.database_connection import SessionLocal
from models.models import Customers
from logger_config import logger


def get_customer_by_id(customer_id: str):
    session = SessionLocal()

    try:
        stmt = select(Customers).where(Customers.customer_id == customer_id)

        customer = session.scalar(stmt)

        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        return customer

    except Exception as e:
        logger.error("Failed to fetch customer", e)
        raise e

    finally:
        session.close()
