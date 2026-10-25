import re
import pandas as pd

from configs.settings import (
    REJECTED_PRODUCTS_FILE,
    REJECTED_STORES_FILE,
    REJECTED_CUSTOMERS_FILE,
    REJECTED_SALES_FILE,
    REJECTED_INVENTORY_FILE,
)

from logger_config import logger


EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def validate_products(product_df):
    logger.info("Products Validation Started")

    valid_records = []
    invalid_records = []

    product_df["unit_price"] = pd.to_numeric(product_df["unit_price"], errors="coerce")

    duplicate_products = set(
        product_df.loc[
            product_df["product_id"].duplicated(keep=False),
            "product_id",
        ]
    )

    for _, row in product_df.iterrows():
        if pd.isna(row["product_id"]):
            invalid_records.append(row)
            continue

        if row["product_id"] in duplicate_products:
            invalid_records.append(row)
            continue

        if pd.isna(row["product_name"]):
            invalid_records.append(row)
            continue

        if pd.isna(row["unit_price"]) or row["unit_price"] <= 0:
            invalid_records.append(row)
            continue

        valid_records.append(row)

    valid_df = pd.DataFrame(valid_records)
    invalid_df = pd.DataFrame(invalid_records)

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_PRODUCTS_FILE, index=False)

    logger.info(f"VALID PRODUCT RECORDS : {len(valid_df)}")
    logger.info(f"INVALID PRODUCT RECORDS : {len(invalid_df)}")

    return valid_df


def validate_stores(stores_df):
    logger.info("Stores Validation Started")

    valid_records = []
    invalid_records = []

    duplicate_stores = set(
        stores_df.loc[
            stores_df["store_id"].duplicated(keep=False),
            "store_id",
        ]
    )

    for _, row in stores_df.iterrows():
        if pd.isna(row["store_id"]):
            invalid_records.append(row)
            continue

        if row["store_id"] in duplicate_stores:
            invalid_records.append(row)
            continue

        if pd.isna(row["store_name"]):
            invalid_records.append(row)
            continue

        if pd.isna(row["city"]):
            invalid_records.append(row)
            continue

        valid_records.append(row)

    valid_df = pd.DataFrame(valid_records)
    invalid_df = pd.DataFrame(invalid_records)

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_STORES_FILE, index=False)

    logger.info(f"VALID STORE RECORDS : {len(valid_df)}")
    logger.info(f"INVALID STORE RECORDS : {len(invalid_df)}")

    return valid_df


def validate_customers(customers_df):
    logger.info("Customers Validation Started")

    valid_records = []
    invalid_records = []

    duplicate_customers = set(
        customers_df.loc[
            customers_df["customer_id"].duplicated(keep=False),
            "customer_id",
        ]
    )

    for _, row in customers_df.iterrows():
        if pd.isna(row["customer_id"]):
            invalid_records.append(row)
            continue

        if row["customer_id"] in duplicate_customers:
            invalid_records.append(row)
            continue

        if pd.isna(row["customer_name"]):
            invalid_records.append(row)
            continue

        if pd.isna(row["email"]):
            invalid_records.append(row)
            continue

        if not re.match(EMAIL_PATTERN, str(row["email"])):
            invalid_records.append(row)
            continue

        valid_records.append(row)

    valid_df = pd.DataFrame(valid_records)
    invalid_df = pd.DataFrame(invalid_records)

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_CUSTOMERS_FILE, index=False)

    logger.info(f"VALID CUSTOMER RECORDS : {len(valid_df)}")
    logger.info(f"INVALID CUSTOMER RECORDS : {len(invalid_df)}")

    return valid_df


def validate_sales(sales_df, products_df, stores_df, customers_df):
    logger.info("Sales Validation Started")

    valid_records = []
    invalid_records = []


    sales_df["quantity"] = pd.to_numeric(sales_df["quantity"], errors="coerce")

    duplicate_sales = set(
        sales_df.loc[
            sales_df["sale_id"].duplicated(keep=False),
            "sale_id",
        ]
    )

    valid_products = set(products_df["product_id"])
    valid_stores = set(stores_df["store_id"])
    valid_customers = set(customers_df["customer_id"])

    for _, row in sales_df.iterrows():
        if pd.isna(row["sale_id"]):
            invalid_records.append(row)
            continue

        if row["sale_id"] in duplicate_sales:
            invalid_records.append(row)
            continue

        if pd.isna(row["product_id"]):
            invalid_records.append(row)
            continue

        if row["product_id"] not in valid_products:
            invalid_records.append(row)
            continue

        if pd.isna(row["store_id"]):
            invalid_records.append(row)
            continue

        if row["store_id"] not in valid_stores:
            invalid_records.append(row)
            continue

        if pd.isna(row["customer_id"]):
            invalid_records.append(row)
            continue

        if row["customer_id"] not in valid_customers:
            invalid_records.append(row)
            continue

        if pd.isna(row["sale_date"]):
            invalid_records.append(row)
            continue

        if pd.isna(row["quantity"]) or row["quantity"] <= 0:
            invalid_records.append(row)
            continue

        valid_records.append(row)

    valid_df = pd.DataFrame(valid_records)
    invalid_df = pd.DataFrame(invalid_records)

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_SALES_FILE, index=False)

    logger.info(f"VALID SALES RECORDS : {len(valid_df)}")
    logger.info(f"INVALID SALES RECORDS : {len(invalid_df)}")

    return valid_df


def validate_inventory(inventory_df, products_df, stores_df):
    logger.info("Inventory Validation Started")

    valid_records = []
    invalid_records = []

    valid_products = set(products_df["product_id"].astype(str))
    valid_stores = set(stores_df["store_id"].astype(str))

    inventory_df["available_quantity"] = pd.to_numeric(
        inventory_df["available_quantity"], errors="coerce"
    )
    inventory_df["reorder_level"] = pd.to_numeric(
        inventory_df["reorder_level"], errors="coerce"
    )

    for _, row in inventory_df.iterrows():
        prod_id = str(row["product_id"])
        store_id = str(row["store_id"])

        if pd.isna(row["product_id"]) or prod_id == "nan" or prod_id not in valid_products:
            invalid_records.append(row)
            continue

        if pd.isna(row["store_id"]) or store_id == "nan" or store_id not in valid_stores:
            invalid_records.append(row)
            continue

        if pd.isna(row["available_quantity"]) or row["available_quantity"] < 0:
            invalid_records.append(row)
            continue

        if pd.isna(row["reorder_level"]) or row["reorder_level"] < 0:
            invalid_records.append(row)
            continue

        valid_records.append(row)

    valid_df = pd.DataFrame(valid_records, columns=inventory_df.columns)
    invalid_df = pd.DataFrame(invalid_records, columns=inventory_df.columns)

    if not invalid_df.empty:
        invalid_df.to_csv(REJECTED_INVENTORY_FILE, index=False)

    logger.info(f"VALID INVENTORY RECORDS : {len(valid_df)}")
    logger.info(f"INVALID INVENTORY RECORDS : {len(invalid_df)}")

    return valid_df
