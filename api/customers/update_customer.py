from fastapi import HTTPException
from sqlalchemy import select

from database.database_connection import sessionLocal
from models.models import Customers
from schemas.schemas import CustomerUpdate


def update_customer(customer_id: str, customer: CustomerUpdate):
    db = sessionLocal()

    try:
        db_customer = db.execute(
            select(Customers).where(Customers.customer_id == customer_id)
        ).scalar_one_or_none()

        if db_customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        for key, value in customer.model_dump().items():
            setattr(db_customer, key, value)

        db.commit()
        db.refresh(db_customer)

        return db_customer

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
