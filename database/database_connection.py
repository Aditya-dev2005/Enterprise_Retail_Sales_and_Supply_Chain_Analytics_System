from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

from configs.settings import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USERNAME
)

database_url = URL.create(
    drivername="mysql+pymysql",
    host=DB_HOST,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(
    database_url,
    echo=False 
)

sessionLocal = sessionmaker(
    bind=engine
)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()