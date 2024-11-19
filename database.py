from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+mysqlconnector://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_DB_URL:YOUR_DB_PORT/YOUR_DB_NAME"

# Initialize database engine by using MySQL
engine = create_engine(DB_URL,echo=True)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

# Create the base class for all ORM models
# The Base object serves as the parent for all database models you define in your application.
Base = declarative_base()