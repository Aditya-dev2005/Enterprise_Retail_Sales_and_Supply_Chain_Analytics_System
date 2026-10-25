from fastapi import HTTPException
from database.database_connection import sessionLocal
from models.models import Sales
from logger_config import logger


def delete_sale(sale_id: str):
    session = sessionLocal()
    try:
        logger.info(f"Deleting Sale with sale_id: {sale_id}....")
        sale = session.get(Sales, sale_id)
        if not sale:
            logger.warning(f"Sale with sale_id: {sale_id} not found")
            raise HTTPException(status_code=404, detail="Sale not found")

        session.delete(sale)
        session.commit()
        logger.info(f"Sale with sale_id: {sale_id} Deleted...")
        return {"detail": f"Sale {sale_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.exception(f"Exception occured while deleting sale {sale_id} : {e}")
        raise HTTPException(status_code=500, detail="Error deleting sale")
    finally:
        session.close()
