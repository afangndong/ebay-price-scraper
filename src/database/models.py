from sqlalchemy import create_engine, Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(String, primary_key=True)
    title = Column(String)
    price = Column(Float)
    platform = Column(String)
    product_name = Column(String)
    link = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
