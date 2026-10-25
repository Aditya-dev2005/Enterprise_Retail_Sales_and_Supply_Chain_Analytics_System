from models.models import Base 
from database.database_connection import sessionLocal,engine
from logger_config import logger 
def create_tables():
    try:
        logger.info("Creation of tables started....")
        Base.metadata.create_all(bind=engine)
        logger.info("All Tables Created Succesfully in Database...")
    except Exception as e:
        logger.info(f"Database Connectivity Failed : {e}")
        print("Couldn't create tables, check Logs for further information.")


if __name__ == "__main__":
    create_tables()