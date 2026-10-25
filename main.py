from fastapi import FastAPI

from api.AnalyticsAPI.router_analytics import router as analytics_router
from api.customers.customer_routes import router as customer_router

from api.products.product_routes import product_router
from api.sales.router import router as sales_router
from api.inventory.inventory_routes import inventory_router
from api.stores.store_routes import router as store_router
from api.pipeline.pipeline_routes import router as pipeline_router
from api.ai.ai_routes import router as ai_router
from api.auth.auth_routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(store_router)
app.include_router(sales_router)
app.include_router(analytics_router)
app.include_router(product_router)
app.include_router(customer_router)
app.include_router(inventory_router)
app.include_router(pipeline_router)
app.include_router(ai_router)
