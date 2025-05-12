# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:newpassword@localhost/hustlehub_db" # update your actual database URL here

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# THIS is what was missing!
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
