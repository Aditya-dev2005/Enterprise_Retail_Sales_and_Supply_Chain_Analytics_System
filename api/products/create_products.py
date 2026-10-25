from fastapi import HTTPException
from database.database_connection import sessionLocal
from models.models import Products
from schemas.schemas import ProductCreate


def create_products(product: ProductCreate):
    session = sessionLocal()

    try:
        new_product = Products(
            product_name=product.product_name,
            brand=product.brand,
            category=product.category,
            status=product.status,
            unit_price=product.unit_price,
            supplier_id=product.supplier_id,
        )

        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product

    except HTTPException as h:
        session.rollback()
        return {"FastAPI Error Occured": f"{h}"}
    except Exception as e:
        session.rollback()
        return {"Exception Occured": f"{e}"}

    finally:
        session.close()
