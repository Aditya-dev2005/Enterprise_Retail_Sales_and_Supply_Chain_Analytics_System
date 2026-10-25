from sqlalchemy import select
from database.database_connection import SessionLocal
from models.models import Stores


def get_all_stores():
    session = SessionLocal()

    try:
        statement = select(Stores)
        stores = session.scalars(statement).all()

        return stores

    finally:
        session.close()