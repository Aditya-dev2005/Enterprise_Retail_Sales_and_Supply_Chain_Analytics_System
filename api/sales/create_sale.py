from fastapi import HTTPException
from database.database_connection import sessionLocal
from models.models import Sales
from schemas.schemas import SaleCreate
from sqlalchemy.exc import IntegrityError
from logger_config import logger


def create_sale(sale_data: SaleCreate):
    session = sessionLocal()
    try:
        logger.info(f"Creating Sale with sale_id: {sale_data.sale_id}....")
        new_sale = Sales(**sale_data.model_dump())
        session.add(new_sale)
        session.commit()
        session.refresh(new_sale)
        logger.info(f"Sale with sale_id: {sale_data.sale_id} Created...")
        return new_sale
    except IntegrityError as e:
        session.rollback()
        logger.exception(f"Integrity error while creating sale {sale_data.sale_id} : {e}")
        raise HTTPException(status_code=400, detail="Sale already exists or invalid reference (product/store/customer)")
    except Exception as e:
        session.rollback()
        logger.exception(f"Exception occured while creating sale {sale_data.sale_id} : {e}")
        raise HTTPException(status_code=500, detail="Error creating sale")
    finally:
        session.close()
