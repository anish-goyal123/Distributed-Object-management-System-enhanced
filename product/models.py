from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    product_name = Column(String(100), index=True)
    product_quantity = Column(Integer)