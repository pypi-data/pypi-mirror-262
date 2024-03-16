from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Integer,
)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve the database URL from the environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

# setting db echo=True - sql query, False, "debug" - response
DB_ECHO = os.getenv("DB_ECHO")
if DB_ECHO != "debug":
    DB_ECHO = bool(DB_ECHO)

# Create the database engine using the specified URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=100, max_overflow=20, echo=DB_ECHO
)
engine.execute("CREATE SCHEMA IF NOT EXISTS api_error_log_schema")

# Create a session factory using the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a base class for declarative models
Base = declarative_base()


class ApiErrorLog(Base):
    __tablename__ = "api_error_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    error_id = Column(String, unique=True, nullable=False)
    api_title = Column(String)
    query_params = Column(Text)
    path_params = Column(Text)
    req_body = Column(Text)
    headers = Column(Text)
    api_url = Column(String)
    traceback = Column(Text)
    personalized_message = Column(Text)
    client_ip = Column(String)
    status_code = Column(Integer)
    status = Column(String, default="Fresh")
    req_time = Column(DateTime)