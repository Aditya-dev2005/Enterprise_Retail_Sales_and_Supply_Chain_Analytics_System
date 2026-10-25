from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database_connection import sessionLocal
from logger_config import logger

from api.AnalyticsAPI.top_products import get_top_products
from api.AnalyticsAPI.store_sales import get_store_sales
from api.AnalyticsAPI.daily_sales import get_daily_sales


router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    logger.info("GET /api/analytics/top-products called")

    return get_top_products(db)


@router.get("/store-sales")
def store_sales(db: Session = Depends(get_db)):
    logger.info("GET /api/analytics/store-sales called")

    return get_store_sales(db)


@router.get("/daily-sales")
def daily_sales(db: Session = Depends(get_db)):
    logger.info("GET /api/analytics/daily-sales called")

    return get_daily_sales(db)
