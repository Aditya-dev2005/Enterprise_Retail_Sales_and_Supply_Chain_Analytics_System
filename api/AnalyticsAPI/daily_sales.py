from sqlalchemy.orm import Session
from sqlalchemy import func

from models.models import Sales, Products
from logger_config import logger


def get_daily_sales(db: Session):

    logger.info("Daily sales analytics started")

    try:
        result = (
            db.query(
                Sales.sale_date,
                func.sum(
                    Sales.quantity * Products.unit_price
                ).label("total_sales")
            )
            .join(
                Products,
                Products.product_id == Sales.product_id
            )
            .group_by(
                Sales.sale_date
            )
            .order_by(
                Sales.sale_date
            )
            .all()
        )

        logger.info(
            "Daily sales analytics completed successfully"
        )

        return [
            {
                "sale_date": row.sale_date,
                "total_sales": row.total_sales
            }
            for row in result
        ]

    except Exception as e:
        logger.error(
            f"Error in daily sales analytics: {e}"
        )
        raise