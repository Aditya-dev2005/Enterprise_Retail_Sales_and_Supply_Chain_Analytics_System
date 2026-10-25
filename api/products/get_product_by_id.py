from fastapi import HTTPException
from database.database_connection import sessionLocal 
from models.models import Products
from schemas.schemas import ProductResponse
from sqlalchemy import select 
from logger_config import logger

def get_products_by_id(product_id:str):
    session = sessionLocal()
    try:
        product = session.scalar(select(Products).where(Products.product_id == product_id))
        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )   

        return product

    except Exception as e:
        logger.exception(f"Exception occurred while fetching the product: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch the product."
        )

    finally:
        session.close()