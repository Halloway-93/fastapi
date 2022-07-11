import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# This is what you put in your sqlalchemy db url :
# postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="Fuckyou",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was succeful!")
        break

    except Exception as error:

        print("Connection to Database failed.")
        print("Error:", error)
        time.sleep(2)
