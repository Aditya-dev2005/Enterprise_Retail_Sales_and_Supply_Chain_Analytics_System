from sqlalchemy import select

from database.database_connection import SessionLocal
from models.models import Stores
from schemas.schemas import StoreCreate
from logger_config import logger


def create_store(store: StoreCreate):

    session = SessionLocal()

    try:

        logger.info(
            f"Creating Store with ID: {store.store_id}"
        )

        statement = select(Stores).where(
            Stores.store_id == store.store_id
        )

        existing_store = session.scalar(statement)

        if existing_store:
            logger.warning(
                f"Store with ID {store.store_id} already exists"
            )

            return

        new_store = Stores(
            store_id=store.store_id,
            store_name=store.store_name,
            city=store.city,
            state=store.state,
            store_manager=store.store_manager,
            opening_date=store.opening_date,
            status=store.status
        )

        session.add(new_store)

        session.commit()

        session.refresh(new_store)

        logger.info(
            f"Store {new_store.store_id} created successfully"
        )

        return new_store

    except Exception as e:

        session.rollback()

        logger.exception(
            f"Failed to create Store {store.store_id}: {e}"
        )

        raise e

    finally:

        session.close()