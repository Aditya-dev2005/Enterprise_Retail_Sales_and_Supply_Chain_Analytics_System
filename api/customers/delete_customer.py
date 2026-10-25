from fastapi import HTTPException
from sqlalchemy import select

from database.database_connection import sessionLocal
from models.models import Customers


def delete_customer(customer_id: str):
    db = sessionLocal()

    try:
        customer = db.execute(
            select(Customers).where(Customers.customer_id == customer_id)
        ).scalar_one_or_none()

        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

        db.delete(customer)
        db.commit()

        return {"message": "Customer deleted successfully"}

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        db.close()
