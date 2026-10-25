from fastapi import HTTPException
from sqlalchemy import select

from database.database_connection import sessionLocal
from models.models import Products
from logger_config import logger


def deactivate_product(prod_id: str):

    session = sessionLocal()

    try:
        logger.info(f"Deactivating Product with ID: {prod_id}")

        prod = session.scalar(select(Products).where(Products.product_id == prod_id))

        if prod is None:
            logger.warning(f"Product with ID {prod_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found.")

        if prod.status == "Inactive":
            logger.warning(f"Product with ID {prod_id} is already inactive.")
            raise HTTPException(status_code=400, detail="Product is already inactive.")

        prod.status = "Inactive"

        session.commit()
        session.refresh(prod)

        logger.info(f"Product with ID {prod_id} deactivated successfully.")

        return {"message": "Product deactivated successfully.", "product": prod}

    except HTTPException:
        raise

    except Exception as e:
        session.rollback()
        logger.exception(f"Error while deactivating Product with ID {prod_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to deactivate product.")

    finally:
        session.close()
