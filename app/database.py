# database connection
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:qpzm@localhost:5432/clozeencounters"
)
# connect to PostgreSQL
engine = create_engine(
    DATABASE_URL, echo=False
)  # echo=True for terminal output for PostgreSQL queries

# session factory using the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base parent model for ORMs
Base = declarative_base()
