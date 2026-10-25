import pandas as pd

from database.database_connection import sessionLocal
from models.models import Products, Stores, Customers, Sales, Inventory

from logger_config import logger


def load_products(products_df):
    session = sessionLocal()

    try:
        for i in range(len(products_df)):
            row = products_df.iloc[i]

            product_id = row["product_id"]

            if session.get(Products, product_id) is None:
                product = Products(
                    product_id=product_id,
                    product_name=row["product_name"],
                    category=row["category"],
                    brand=row["brand"],
                    unit_price=float(row["unit_price"]),
                    supplier_id=row["supplier_id"],
                    status=row["status"],
                )

                session.add(product)

        session.commit()

        logger.info("Products Loaded Successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading products: {e}")
        raise

    finally:
        session.close()


def load_stores(stores_df):
    session = sessionLocal()

    try:
        stores_df["opening_date"] = pd.to_datetime(
            stores_df["opening_date"], errors="coerce"
        ).dt.date

        for i in range(len(stores_df)):
            row = stores_df.iloc[i]

            store_id = row["store_id"]

            if session.get(Stores, store_id) is None:
                store = Stores(
                    store_id=store_id,
                    store_name=row["store_name"],
                    city=row["city"],
                    state=row["state"],
                    store_manager=row["store_manager"],
                    opening_date=row["opening_date"],
                    status=row["status"],
                )

                session.add(store)

        session.commit()

        logger.info("Stores Loaded Successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading stores: {e}")
        raise

    finally:
        session.close()


def load_customers(customers_df):
    session = sessionLocal()

    try:
        customers_df["registration_date"] = pd.to_datetime(
            customers_df["registration_date"], errors="coerce"
        ).dt.date

        for i in range(len(customers_df)):
            row = customers_df.iloc[i]

            customer_id = row["customer_id"]

            if session.get(Customers, customer_id) is None:
                customer = Customers(
                    customer_id=customer_id,
                    customer_name=row["customer_name"],
                    email=row["email"],
                    mobile=str(row["mobile"]),
                    city=row["city"],
                    registration_date=row["registration_date"],
                    customer_type=row["customer_type"],
                )

                session.add(customer)

        session.commit()

        logger.info("Customers Loaded Successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading customers: {e}")
        raise

    finally:
        session.close()


def load_sales(sales_df):
    session = sessionLocal()

    try:
        sales_df["sale_date"] = pd.to_datetime(
            sales_df["sale_date"], errors="coerce"
        ).dt.date

        for i in range(len(sales_df)):
            row = sales_df.iloc[i]

            sale_id = row["sale_id"]

            if session.get(Sales, sale_id) is None:
                sale = Sales(
                    sale_id=sale_id,
                    product_id=row["product_id"],
                    store_id=row["store_id"],
                    customer_id=row["customer_id"],
                    quantity=int(row["quantity"]),
                    sale_date=row["sale_date"],
                    discount_percentage=float(row["discount_percentage"]),
                    payment_mode=row["payment_mode"],
                )

                session.add(sale)

        session.commit()

        logger.info("Sales Loaded Successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading sales: {e}")
        raise

    finally:
        session.close()


def load_inventory(inventory_df):
    session = sessionLocal()

    try:
        inventory_df["last_updated"] = pd.to_datetime(
            inventory_df["last_updated"], errors="coerce"
        ).dt.date

        for i in range(len(inventory_df)):
            row = inventory_df.iloc[i]

            inventory_id = row["inventory_id"]

            if session.get(Inventory, inventory_id) is None:
                inventory = Inventory(
                    inventory_id=inventory_id,
                    product_id=row["product_id"],
                    store_id=row["store_id"],
                    available_quantity=int(row["available_quantity"]),
                    reorder_level=int(row["reorder_level"]),
                    last_updated=row["last_updated"],
                )

                session.add(inventory)

        session.commit()

        logger.info("Inventory Loaded Successfully")

    except Exception as e:
        session.rollback()
        logger.error(f"Error loading inventory: {e}")
        raise

    finally:
        session.close()
