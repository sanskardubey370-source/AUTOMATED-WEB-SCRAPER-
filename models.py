from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Setup SQLite Database
engine = create_engine('sqlite:///scraped_data.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=True)
    source_url = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

# Initialize the database (creates tables if they don't exist)
def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")