import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus

load_dotenv(os.path.join(os.getcwd(), ".env"))

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "business_kpi")

def get_engine(echo: bool = False):
    if not DB_USER:
        raise RuntimeError("DB_USER not set in .env")
    pw = quote_plus(DB_PASS)            # <-- encodes @ : % etc.
    uri = f"mysql+pymysql://{DB_USER}:{pw}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(uri, echo=echo, pool_recycle=3600, future=True)

def test_connection():
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar_one()
            print("Database reachable - test query returned:", result)
    except Exception as e:
        print("Database connection failed")
        print("error:", e)

if __name__ == "__main__":
    test_connection()
