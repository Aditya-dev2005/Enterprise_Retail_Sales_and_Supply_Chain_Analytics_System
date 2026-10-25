import pandas as pd

from configs.settings import (
    PRODUCT_FILE,
    SALES_FILE,
    STORE_FILE,
    INVENTORY_FILE,
    CUSTOMER_FILE
)

from logger_config import logger


def extract_products():
    try:
        logger.info("Extracting Products File...")
        products_df = pd.read_csv(PRODUCT_FILE)
        return products_df
    except Exception as e:
        logger.exception(f"Couldn't extract Products Table: {e}")


def extract_sales():
    try:
        logger.info("Extracting Sales File...")
        sales_df = pd.read_csv(SALES_FILE)
        return sales_df
    except Exception as e:
        logger.exception(f"Couldn't extract Sales Table: {e}")


def extract_stores():
    try:
        logger.info("Extracting Stores File...")
        stores_df = pd.read_csv(STORE_FILE)
        return stores_df
    except Exception as e:
        logger.exception(f"Couldn't extract Stores Table: {e}")


def extract_inventory():
    try:
        logger.info("Extracting Inventory File...")
        inventory_df = pd.read_csv(INVENTORY_FILE)
        return inventory_df
    except Exception as e:
        logger.exception(f"Couldn't extract Inventory Table: {e}")


def extract_customer():
    try:
        logger.info("Extracting Customer File...")
        customer_df = pd.read_csv(CUSTOMER_FILE)
        return customer_df
    except Exception as e:
        logger.exception(f"Couldn't extract Customers Table: {e}")