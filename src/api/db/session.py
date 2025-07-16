import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL, DB_TIMEZONE
import timescaledb


if DATABASE_URL == "":
   raise ValueError("DATABASE_URL must be set in the environment variables.")
engine = timescaledb.create_engine(DATABASE_URL, timezone=DB_TIMEZONE)



def init_db():
   print("Initializing database connection...")
   SQLModel.metadata.create_all(engine)
   print('createing hypertable')
   timescaledb.metadata.create_all(engine)

def get_session():      #to be used in the API routes , providing a database session
   with Session(engine) as session:
      yield session 