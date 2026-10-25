from sqlalchemy import select
from database.database_connection import SessionLocal
from models.models import Stores
from schemas.schemas import StoreUpdate


def update_store(store_id: str, store_data: StoreUpdate):
    session = SessionLocal()

    try:
        statement = select(Stores).where(Stores.store_id == store_id)

        store = session.scalar(statement)

        if not store:
            return

        if store_data.store_name is not None:
            store.store_name = store_data.store_name

        if store_data.city is not None:
            store.city = store_data.city

        if store_data.state is not None:
            store.state = store_data.state

        if store_data.store_manager is not None:
            store.store_manager = store_data.store_manager

        if store_data.opening_date is not None:
            store.opening_date = store_data.opening_date

        if store_data.status is not None:
            store.status = store_data.status

        session.commit()
        session.refresh(store)

        return store

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()
