from sqlalchemy import Column, Integer, String, Float
from app.database.base import Base

class Stocks(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True)
    purchased_amount = Column(Float)
    purchased_status = Column(String)
    request_date = Column(String)
    stock_symbol = Column(String)