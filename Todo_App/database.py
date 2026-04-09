from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# engine: helps connect to database : Engine = thing that connects your app to the database
# sessionmaker → creates DB sessions
# declarative_base → used to define tables
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db" # db_type, path format , file name in current folder

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # important for SQLite , Needed for SQLite because: FastAPI handles multiple requests, SQLite by default allows only one thread, So we say :“Allow multiple threads”
) # This creates connection to DB

SessionLocal = sessionmaker(
    autocommit=False, # manually save changes
    autoflush=False, # dont auto send changes to db
    bind=engine # connect session to db engine
) # This creates a session : A session = a temporary connection to talk to DB

Base = declarative_base() # This is used to create tables (models)