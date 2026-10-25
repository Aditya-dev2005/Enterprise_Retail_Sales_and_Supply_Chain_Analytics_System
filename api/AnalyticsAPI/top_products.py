from sqlalchemy.orm import Session
from sqlalchemy import func

from models.models import Products, Sales
from logger_config import logger


def get_top_products(db: Session):

    logger.info("Top products analytics started")

    try:
        result = (
            db.query(
                Products.product_id,
                Products.product_name,
                func.sum(Sales.quantity).label("total_quantity_sold"),
            )
            .join(Sales, Products.product_id == Sales.product_id)
            .group_by(Products.product_id, Products.product_name)
            .order_by(func.sum(Sales.quantity).desc())
            .all()
        )

        logger.info("Top products analytics completed successfully")

        return [
            {
                "product_id": row.product_id,
                "product_name": row.product_name,
                "total_quantity_sold": row.total_quantity_sold,
            }
            for row in result
        ]

    except Exception as e:
        logger.error(f"Error in top products analytics: {e}")
        raise
