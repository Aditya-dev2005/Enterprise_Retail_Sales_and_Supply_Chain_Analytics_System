from sqlalchemy import select
from database.database_connection import sessionLocal
from models.models import Customers


def get_all_customers():
    session = sessionLocal()
    try:
        statement = select(Customers)
        customers = session.scalars(statement).all()
        return customers
    finally:
        session.close()
