from sqlalchemy import select
from database.database_connection import SessionLocal
from models.models import Stores


def get_store_by_id(store_id: str):
    session = SessionLocal()

    try:
        statement = select(Stores).where(
            Stores.store_id == store_id
        )

        store = session.scalar(statement)

        if not store:
            return

        return store

    finally:
        session.close()