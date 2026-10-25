import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

RAW_FOLDER = "data/raw"

REJECED_FOLDER = "data/rejected"
os.makedirs(REJECED_FOLDER, exist_ok=True)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "Retail_Sales_and_Supply_Chain_Analytics")

PRODUCT_FILE = "data/raw/products.csv"
STORE_FILE = "data/raw/stores.csv"
SALES_FILE = "data/raw/sales.csv"
INVENTORY_FILE = "data/raw/inventory.csv"
CUSTOMER_FILE = "data/raw/customers.csv"

REJECTED_PRODUCTS_FILE = "data/rejected/rejected_products.csv"

REJECTED_STORES_FILE = "data/rejected/rejected_stores.csv"

REJECTED_SALES_FILE = "data/rejected/rejected_sales.csv"

REJECTED_INVENTORY_FILE = "data/rejected/rejected_inventory.csv"

REJECTED_CUSTOMERS_FILE = "data/rejected/rejected_customers.csv"

# -------------------- AI Query Endpoint (OpenRouter) --------------------
# Get a free key at https://openrouter.ai/keys and set it as an
# environment variable named OPENROUTER_API_KEY (or put it in a local
# .env file - never commit the real key to GitHub).
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# You can point this at any model available on OpenRouter. Several
# free models are available (their catalog marks them with ":free").
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free"
)

# -------------------- Authentication (JWT) --------------------
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES", "60"))
