from fastapi import HTTPException
from database.database_connection import sessionLocal
from models.models import Sales
from schemas.schemas import SaleUpdate
from logger_config import logger


def update_sale(sale_id: str, sale_data: SaleUpdate):
    session = sessionLocal()
    try:
        logger.info(f"Updating Sale with sale_id: {sale_id}....")
        sale = session.get(Sales, sale_id)
        if not sale:
            logger.warning(f"Sale with sale_id: {sale_id} not found")
            raise HTTPException(status_code=404, detail="Sale not found")

        for field, value in sale_data.model_dump().items():
            setattr(sale, field, value)

        session.commit()
        session.refresh(sale)
        logger.info(f"Sale with sale_id: {sale_id} Updated...")
        return sale
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.exception(f"Exception occured while updating sale {sale_id} : {e}")
        raise HTTPException(status_code=500, detail="Error updating sale")
    finally:
        session.close()
