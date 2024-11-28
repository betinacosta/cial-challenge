from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import exc
import logging

from app.database.models import Stocks
from app.database.base import Base

load_dotenv()

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

class PostgresDB:

    def __init__(self):
        db_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        logging.info("Attempting database connection")
        try:
            engine = create_engine(db_string)
            Base.metadata.create_all(engine, checkfirst=True)
            connection = engine.connect()
            logging.info("Database connection was successful")
        except exc.SQLAlchemyError as err:
            logging.error(f"Cannot connect to database: {err}")
            raise err

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_stock(self, stock_purchase):
        stock = self.read_stock(stock_purchase.get("stock_symbol"))
        if stock:
            stock_purchase["id"] = stock.id
            return self.update_stock(stock_purchase)
        else:
            return self.add_stock(stock_purchase)

    def add_stock(self, stock_purchase):
        row = Stocks(
            purchased_amount=stock_purchase.get("purchased_amount"),
            purchased_status=stock_purchase.get("purchased_status"),
            request_date=stock_purchase.get("request_date"),
            stock_symbol=stock_purchase.get("stock_symbol"),
        )
        try:
            self.session.add(row)
            self.session.commit()
            logging.info("Stock added successfully")
            status = 201
        except exc.SQLAlchemyError as err:
            logging.error(f"Error while adding purchase to database: {err}")
            status = 500
        self.session.close()
        return status

    def read_stock(self, symbol):
        stock = self.session.query(Stocks).filter_by(stock_symbol = symbol).first()
        self.session.close()
        return stock

    def update_stock(self, stock_purchase):
        stock = self.session.get(Stocks, stock_purchase.get("id"))

        stock.purchased_amount = stock_purchase.get("purchased_amount")
        stock.purchased_status = stock_purchase.get("purchased_status")
        stock.request_date = stock_purchase.get("request_date")
        stock.stock_symbol = stock_purchase.get("stock_symbol")
        try:
            self.session.commit()
            logging.info("Stock updated successfully")
            status = 200
        except exc.SQLAlchemyError as err:
            logging.error(f"Error while adding purchase to database: {err}")
            status = 500

        self.session.close()
        return status





