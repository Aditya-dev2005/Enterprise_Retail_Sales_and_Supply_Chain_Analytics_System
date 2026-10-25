from fastapi import HTTPException
from database.database_connection import sessionLocal 
from models.models import Products
from schemas.schemas import ProductResponse
from sqlalchemy import select 
from logger_config import logger
def get_products():
    session = sessionLocal()
    try:
        logger.info("Getting all the Products....")
        products = session.scalars(select(Products)).all()
        logger.info("All Products Fetched...")
        return products
    except Exception as e:
        logger.exception(f"Exception occurred while fetching the products: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch products."
        )
    finally:
        session.close()