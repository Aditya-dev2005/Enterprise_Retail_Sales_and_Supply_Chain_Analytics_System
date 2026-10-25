from typing import List
from sqlalchemy import select
from fastapi import HTTPException, status

from database.database_connection import sessionLocal
from models.models import Inventory
from logger_config import logger


def get_all_inventory() -> List[Inventory]:
    session = sessionLocal()
    try:
        stmt = select(Inventory)
        inventory_items = session.scalars(stmt).all()
        logger.info(f"Retrieved {len(inventory_items)} inventory records")
        return inventory_items
    except Exception as e:
        logger.error("Failed to fetch inventory records", exc_info=True)
        raise e
    finally:
        session.close()


def get_inventory_by_store(store_id: str) -> List[Inventory]:
    session = sessionLocal()
    try:
        stmt = select(Inventory).where(Inventory.store_id == store_id)
        inventory_items = session.scalars(stmt).all()

        if not inventory_items:
            logger.warning(f"No inventory records found for store_id: {store_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No inventory records found for store_id: '{store_id}'"
            )

        logger.info(f"Retrieved {len(inventory_items)} inventory records for store {store_id}")
        return inventory_items
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch inventory for store_id: {store_id}", exc_info=True)
        raise e
    finally:
        session.close()


def get_low_stock_inventory() -> List[Inventory]:
    session = sessionLocal()
    try:
        stmt = select(Inventory).where(Inventory.available_quantity <= Inventory.reorder_level)
        low_stock_items = session.scalars(stmt).all()
        logger.info(f"Retrieved {len(low_stock_items)} low-stock inventory records")
        return low_stock_items
    except Exception as e:
        logger.error("Failed to fetch low-stock inventory records", exc_info=True)
        raise e
    finally:
        session.close()