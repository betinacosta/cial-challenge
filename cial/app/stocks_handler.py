import json
import logging

from scrapy.utils.serialize import ScrapyJSONEncoder
from datetime import date

from app.polygon_api_handler import PolygonAPIHandler
from app.spider_runner import SpiderRunner
from stocks_crawler.stocks.spiders.stocks_spider import StocksSpider
from app.schemas import stock_model
from app.database.database import PostgresDB

class StocksHandler:
    polygon_api_handler = PolygonAPIHandler()

    def __init__(self, stock_symbol:str):
        self.stock_symbol = stock_symbol
        self.database = PostgresDB()

    def parse_get_stocks(self):
        logging.info("Fetching stocks data from web")
        runner = SpiderRunner()
        deferred = runner.crawl(StocksSpider, stock_symbol=self.stock_symbol)
        deferred.addCallback(self.get_stocks_data)

        return deferred

    def get_stocks_data(self, output) -> json:
        _encoder = ScrapyJSONEncoder()

        market_watch_data = json.loads(_encoder.encode(output))
        polygon_data = self.polygon_api_handler.get_polygon_data(self.stock_symbol)
        database_data = self.database.read_stock(self.stock_symbol)

        if not market_watch_data and not polygon_data:
            return {}

        stock_model["company_code"] = self.stock_symbol
        today = date.today()
        stock_model["request_date"] = today.strftime('%Y-%m-%d')
        market_watch_data = market_watch_data[0]

        if database_data:
            stock_model["purchased_amount"] = database_data.purchased_amount
            stock_model["purchased_status"] = database_data.purchased_status

        if polygon_data:
            stock_model["stock_values"] = {
                "open": polygon_data.get("open"),
                "high": polygon_data.get("high"),
                "low": polygon_data.get("low"),
                "close": polygon_data.get("close")
            }
            stock_model["status"] = polygon_data.get("status")

        if market_watch_data:
            stock_model["performance_data"] = {
                "five_days": market_watch_data.get("five_days"),
                "one_month": market_watch_data.get("one_month"),
                "three_months": market_watch_data.get("three_months"),
                "year_to_date": market_watch_data.get("year_to_date"),
                "one_year": market_watch_data.get("one_year"),
            }
            stock_model["competitors"] = market_watch_data.get("competitors")
            stock_model["market_cap"] = market_watch_data.get("market_cap")
            stock_model["company_name"] = market_watch_data.get("company_name")

        return json.dumps(stock_model)

    def parse_post_stocks(self, amount:float) -> int:
        stock_purchase = {
            "purchased_amount": amount,
            "purchased_status": "purchased",
            "request_date": date.today(),
            "stock_symbol": self.stock_symbol
        }
        response = self.database.create_stock(stock_purchase)
        return response


    def get_stocks_from_cache(self):
        return None
