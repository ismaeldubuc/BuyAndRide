import psycopg2
import os
import logging
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('PG_HOST', 'hetic.cd5ufp6fsve3.us-east-1.rds.amazonaws.com'),
            port=os.getenv('PG_PORT', '5432'),
            database=os.getenv('PG_DB', 'groupe4'),
            user=os.getenv('PG_USER', 'postgres'),
            password=os.getenv('PG_PASSWORD', 'LeContinent!')
        )
        logging.info("Database connection successful")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {str(e)}")
        raise 