from fastapi import HTTPException
from database.database_connection import sessionLocal
from models.models import Sales
from schemas.schemas import SaleResponse
from sqlalchemy import select
from logger_config import logger


def get_sales():
    session = sessionLocal()
    try:
        logger.info("Getting all the Sales....")
        sales = session.scalars(select(Sales)).all()
        logger.info("All Sales Fetched...")
        return sales
    except Exception as e:
        logger.exception(f"Exception occured while fetching all the sales : {e}")
    finally:
        session.close()
