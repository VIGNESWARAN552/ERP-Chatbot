from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

def connect_to_database():
    """
    Connects to the PostgreSQL database using SQLAlchemy.
    Returns a session if successful, otherwise prints the error.
    """
    DATABASE_URL = "postgresql+psycopg2://postgres:Vign%402025@localhost:5432/postgres"
    
    try:
        # Create the database engine
        engine = create_engine(DATABASE_URL)
        
        # Bind the engine to a session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Test the connection
        connection = engine.connect()
        connection.close()
        
        print("Connection successful!")
        return session
    
    except SQLAlchemyError as e:
        print("An error occurred while connecting to the database:")
        print(str(e))
        return None
session = connect_to_database()
if session:
    # Proceed with database operations
    pass
    

#SQLAlchemy engine
engine = create_engine("postgresql+psycopg2://postgres:Vign%402025@localhost:5432/postgres")

# SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()    

