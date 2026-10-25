from fastapi import HTTPException
from sqlalchemy import select

from database.database_connection import sessionLocal
from models.models import Products
from schemas.schemas import ProductUpdate
from logger_config import logger


def update_product(prod_id: str, product: ProductUpdate):

    session = sessionLocal()

    try:
        logger.info(f"Updating Product with ID: {prod_id}")

        prod = session.scalar(select(Products).where(Products.product_id == prod_id))

        if prod is None:
            logger.warning(f"Product with ID {prod_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found.")

        if product.product_name is not None:
            prod.product_name = product.product_name

        if product.category is not None:
            prod.category = product.category

        if product.brand is not None:
            prod.brand = product.brand

        if product.unit_price is not None:
            prod.unit_price = product.unit_price

        if product.supplier_id is not None:
            prod.supplier_id = product.supplier_id

        if product.status is not None:
            prod.status = product.status

        session.commit()
        session.refresh(prod)

        logger.info(f"Product with ID {prod_id} updated successfully.")

        return {"message": "Product updated successfully.", "product": prod}

    except HTTPException:
        raise

    except Exception as e:
        session.rollback()
        logger.exception(f"Error while updating Product with ID {prod_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product.")

    finally:
        session.close()
