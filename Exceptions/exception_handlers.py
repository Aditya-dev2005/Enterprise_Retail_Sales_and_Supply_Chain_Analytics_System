from fastapi import Request
from fastapi.responses import JSONResponse

from exceptions.custom_exceptions import (
    ProductNotFoundException,
    StoreNotFoundException,
    CustomerNotFoundException,
    InsufficientInventoryException,
    InvalidSalesException,
    DatabaseException,
    PipelineException
)

from config.logging_config import logger


async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundException
):
    logger.error(
        f"Product not found: {exc.product_id}"
    )

    return JSONResponse(
        status_code=404,
        content={
            "status": "ERROR",
            "message": exc.message
        }
    )


async def store_not_found_handler(
    request: Request,
    exc: StoreNotFoundException
):
    logger.error(
        f"Store not found: {exc.store_id}"
    )

    return JSONResponse(
        status_code=404,
        content={
            "status": "ERROR",
            "message": exc.message
        }
    )


async def customer_not_found_handler(
    request: Request,
    exc: CustomerNotFoundException
):
    logger.error(
        f"Customer not found: {exc.customer_id}"
    )

    return JSONResponse(
        status_code=404,
        content={
            "status": "ERROR",
            "message": exc.message
        }
    )


async def insufficient_inventory_handler(
    request: Request,
    exc: InsufficientInventoryException
):
    logger.error(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "status": "ERROR",
            "message": exc.message
        }
    )


async def invalid_sales_handler(
    request: Request,
    exc: InvalidSalesException
):
    logger.error(exc.message)

    return JSONResponse(
        status_code=400,
        content={
            "status": "ERROR",
            "message": exc.message
        }
    )


async def database_exception_handler(
    request: Request,
    exc: DatabaseException
):
    logger.error(
        f"Database error: {exc.message}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "message": "Database error occurred"
        }
    )


async def pipeline_exception_handler(
    request: Request,
    exc: PipelineException
):
    logger.error(
        f"Pipeline error: {exc.message}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "message": exc.message
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        f"Unexpected error: {exc}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "message": "Internal server error"
        }
    )