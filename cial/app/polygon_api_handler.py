import requests

from datetime import date, timedelta
import os
from dotenv import load_dotenv
import logging

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")


class PolygonAPIHandler:
    polygon_url_base = "https://api.polygon.io/v1/open-close/"
    headers = {
            'Authorization': f'Bearer {POLYGON_API_KEY}',
        }

    def get_polygon_data(self, stock_symbol:str) -> dict:
        yesterday = date.today() - timedelta(days=1)
        stock_symbol = stock_symbol.upper()

        url = f"{self.polygon_url_base}{stock_symbol}/{yesterday}"

        response = requests.get(url=url, headers=self.headers)

        if response.ok:
            logging.info(f"Successfully requested polygon data for {stock_symbol}")
            return response.json()
        logging.error(f"Polygon request failed with {response.status_code}")
        return {}
