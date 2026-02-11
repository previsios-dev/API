from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os
import urllib.parse
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()

raw_password = "8AiwsA8A.Veh@Qc"


safe_password = urllib.parse.quote_plus(raw_password)
DATABASE_URL = f"postgresql://postgres.mhtossnifudvdoauyott:{safe_password}@aws-0-us-west-2.pooler.supabase.com:6543/postgres"
engine = create_engine(DATABASE_URL, poolclass=NullPool)
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()