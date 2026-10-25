from sqlalchemy.orm import Session
from sqlalchemy import func

from models.models import Stores, Sales, Products
from logger_config import logger


def get_store_sales(db: Session):

    logger.info("Store sales analytics started")

    try:
        result = (
            db.query(
                Stores.store_id,
                Stores.store_name,
                func.sum(
                    Sales.quantity * Products.unit_price
                ).label("total_sales")
            )
            .join(
                Sales,
                Stores.store_id == Sales.store_id
            )
            .join(
                Products,
                Products.product_id == Sales.product_id
            )
            .group_by(
                Stores.store_id,
                Stores.store_name
            )
            .order_by(
                func.sum(
                    Sales.quantity * Products.unit_price
                ).desc()
            )
            .all()
        )

        logger.info(
            "Store sales analytics completed successfully"
        )

        return [
            {
                "store_id": row.store_id,
                "store_name": row.store_name,
                "total_sales": row.total_sales
            }
            for row in result
        ]

    except Exception as e:
        logger.error(
            f"Error in store sales analytics: {e}"
        )
        raise