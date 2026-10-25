from fastapi import HTTPException
from database.database_connection import sessionLocal
from models.models import Sales
from schemas.schemas import SaleResponse
from logger_config import logger


def get_sale(sale_id: str):
    session = sessionLocal()
    try:
        logger.info(f"Getting Sale with sale_id: {sale_id}....")
        sale = session.get(Sales, sale_id)
        if not sale:
            logger.warning(f"Sale with sale_id: {sale_id} not found")
            raise HTTPException(status_code=404, detail="Sale not found")
        logger.info(f"Sale with sale_id: {sale_id} Fetched...")
        return sale
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Exception occured while fetching sale {sale_id} : {e}")
        raise HTTPException(status_code=500, detail="Error fetching sale")
    finally:
        session.close()
