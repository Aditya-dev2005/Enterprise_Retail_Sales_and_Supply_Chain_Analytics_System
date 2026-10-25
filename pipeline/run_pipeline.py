from pipeline.extract import (
    extract_inventory,
    extract_products,
    extract_sales,
    extract_stores,
    extract_customer,
)

from pipeline.load import (
    load_inventory,
    load_products,
    load_sales,
    load_stores,
    load_customers,
)

from pipeline.transform import transform_inventory, transform_sales

from pipeline.validate import (
    validate_inventory,
    validate_products,
    validate_sales,
    validate_stores,
    validate_customers,
)

from logger_config import logger


def run_pipeline():

    try:
        logger.info("Pipeline Started")

        print("========================================")
        print("       ENTERPRISE RETAIL PIPELINE")
        print("========================================")

        products_df = extract_products()
        stores_df = extract_stores()
        sales_df = extract_sales()
        inventory_df = extract_inventory()
        customers_df = extract_customer()

        print("\nExtraction Completed")

        print(f"Products Received  : {len(products_df)}")
        print(f"Stores Received    : {len(stores_df)}")
        print(f"Customers Received : {len(customers_df)}")
        print(f"Sales Received     : {len(sales_df)}")
        print(f"Inventory Received : {len(inventory_df)}")

        valid_products_df = validate_products(products_df)

        valid_stores_df = validate_stores(stores_df)

        valid_customers_df = validate_customers(customers_df)

        valid_sales_df = validate_sales(
            sales_df, valid_products_df, valid_stores_df, valid_customers_df
        )

        valid_inventory_df = validate_inventory(
            inventory_df, valid_products_df, valid_stores_df
        )

        print("\nValidation Completed")

        print(f"Valid Products    : {len(valid_products_df)}")
        print(f"Valid Stores      : {len(valid_stores_df)}")
        print(f"Valid Customers   : {len(valid_customers_df)}")
        print(f"Valid Sales       : {len(valid_sales_df)}")
        print(f"Valid Inventory   : {len(valid_inventory_df)}")

        transformed_sales_df = transform_sales(
            valid_sales_df, valid_products_df, valid_stores_df, valid_customers_df
        )

        transformed_inventory_df = transform_inventory(
            valid_inventory_df, valid_sales_df
        )

        print("\nTransformation Completed")

        print(f"Transformed Sales     : {len(transformed_sales_df)}")

        print(f"Transformed Inventory : {len(transformed_inventory_df)}")

        load_products(valid_products_df)

        load_stores(valid_stores_df)

        load_customers(valid_customers_df)

        load_sales(transformed_sales_df)

        load_inventory(transformed_inventory_df)

        print("\nLoad Completed Successfully")

        total_received = (
            len(products_df)
            + len(stores_df)
            + len(customers_df)
            + len(sales_df)
            + len(inventory_df)
        )

        total_loaded = (
            len(valid_products_df)
            + len(valid_stores_df)
            + len(valid_customers_df)
            + len(transformed_sales_df)
            + len(transformed_inventory_df)
        )

        total_rejected = total_received - total_loaded

        print("\n========================================")
        print("          PIPELINE SUMMARY")
        print("========================================")

        print(f"Total Records Received : {total_received}")
        print(f"Total Records Loaded   : {total_loaded}")
        print(f"Total Records Rejected : {total_rejected}")
        print("Pipeline Status        : SUCCESS")

        print("========================================")

        logger.info("Pipeline Completed Successfully")

        return {
            "status": "SUCCESS",
            "products_received": len(products_df),
            "stores_received": len(stores_df),
            "customers_received": len(customers_df),
            "sales_received": len(sales_df),
            "inventory_received": len(inventory_df),
            "products_loaded": len(valid_products_df),
            "stores_loaded": len(valid_stores_df),
            "customers_loaded": len(valid_customers_df),
            "sales_loaded": len(transformed_sales_df),
            "inventory_loaded": len(transformed_inventory_df),
            "total_records_received": total_received,
            "total_records_loaded": total_loaded,
            "total_records_rejected": total_rejected,
        }

    except Exception as e:
        logger.exception(f"Pipeline Failed: {e}")

        print("\n========================================")
        print("          PIPELINE FAILED")
        print("========================================")

        print(f"Error: {e}")

        raise


if __name__ == "__main__":
    run_pipeline()
