from logger_config import logger
import pandas as pd

def transform_sales(sales_df, products_df, stores_df, customers_df):
    logger.info("Sale Transformation Started")
    
    final_sales_df = sales_df.merge(products_df, on="product_id", how="left")
    final_sales_df = final_sales_df.merge(stores_df, on="store_id", how="left")
    final_sales_df = final_sales_df.merge(customers_df, on="customer_id", how="left")

    final_sales_df["gross_amount"] = (
        final_sales_df["quantity"] * final_sales_df["unit_price"]
    )
    
    final_sales_df["discount_amount"] = (
        final_sales_df["gross_amount"] * final_sales_df["discount_percentage"] / 100
    )
    
    final_sales_df["net_amount"] = (
        final_sales_df["gross_amount"] - final_sales_df["discount_amount"]
    )

    sale_category_list = []

    for quantity in final_sales_df["quantity"]:
        if quantity >= 50:
            sale_category_list.append("Bulk Sale")
        elif quantity >= 20:
            sale_category_list.append("Medium Sale")
        else:
            sale_category_list.append("Retail Sale")

    final_sales_df["sale_category"] = sale_category_list

    logger.info("Sales Data Transformed")
    
    return final_sales_df


def transform_inventory(inventory_df, sales_df):
    logger.info("Inventory Transformation Started")
    
    sales_summary = sales_df.groupby(["product_id", "store_id"])["quantity"].sum().reset_index()
    sales_summary = sales_summary.rename(columns={"quantity": "sold_quantity"})
    
    inventory_df = inventory_df.merge(sales_summary, on=["product_id", "store_id"], how="left")
    inventory_df["sold_quantity"] = inventory_df["sold_quantity"].fillna(0)
    
    inventory_df["available_quantity"] = (
        inventory_df["available_quantity"] - inventory_df["sold_quantity"]
    )
    
    inventory_status_list = []

    for i in range(len(inventory_df)):
        row = inventory_df.iloc[i]
        available_quantity = row["available_quantity"]
        reorder_level = row["reorder_level"]
        
        if available_quantity < 0:
            raise ValueError("Negative inventory")
            
        if available_quantity <= reorder_level:
            inventory_status_list.append("REORDER REQUIRED")
        else:
            inventory_status_list.append("AVAILABLE")

    inventory_df["inventory_status"] = inventory_status_list
    inventory_df = inventory_df.drop(columns=["sold_quantity"])
    
    logger.info("Inventory Transformation Completed")
    
    return inventory_df