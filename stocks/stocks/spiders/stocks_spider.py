import scrapy
import logging
import regex
import re
from stocks.items import StocksItem


class StocksSpider(scrapy.Spider):
    name = "stocks_spider"
    market_watch_url = "https://www.marketwatch.com/investing/stock/"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "cache-control": "no-cache",
        "origin": "https://www.marketwatch.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/131.0.0.0 Safari/537.36",
    }

    def __init__(self, stock_symbol: str):
        self.stock_symbol = stock_symbol

    def start_requests(self):
        url = self.market_watch_url + self.stock_symbol
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, headers=self.headers)

    def parse(self, response, **kwargs):
        stocks_item = StocksItem()
        performances_list= response.css('div.performance>table>tbody>tr>td>ul>li.value::text').getall()

        key_data_labels = response.css("ul.list--kv>li>small.label::text").getall()
        key_data_values = response.css("ul.list--kv>li>span.primary::text").getall()

        performances = self.get_performances(performances_list)
        competitors = response.css('div.Competitors>table>tbody>tr>td>a::text').getall()
        key_data = self.get_key_data(key_data_labels, key_data_values)

        stocks_item["five_days"] = performances["five_days"]
        stocks_item["one_month"] = performances["one_month"]
        stocks_item["three_months"] = performances["three_months"]
        stocks_item["year_to_date"] = performances["year_to_date"]
        stocks_item["one_year"] = performances["one_year"]
        stocks_item["competitors"] = competitors
        stocks_item["market_cap"] = self.format_market_cap(key_data.get("Market Cap"))

        return stocks_item

    def get_performances(self, performances_list):
        performances = {
            "five_days": None,
            "one_month": None,
            "three_months": None,
            "year_to_date": None,
            "one_year": None
        }

        idx = 0
        for key in performances:
            try:
                performances[key] = performances_list[idx]
                performances[key] = self.format_performance(performances_list[idx])
            except IndexError:
                logging.warning(f"{key} information not scrapped")
            idx = idx+1

        return performances

    @staticmethod
    def format_performance(raw_performance):
        f_performance = raw_performance.replace("%", "")
        return float(f_performance)

    def format_market_cap(self, raw_makert_cap):
        f_market_cap = {
            "currency": self.get_currency(raw_makert_cap),
            "value": float(re.sub(r'[^0-9.]', '', raw_makert_cap))
        }
        return f_market_cap

    @staticmethod
    def get_key_data(labels, values):
        key_data = {}

        for idx, label in enumerate(labels):
            key_data[label] = values[idx] if idx < len(values) else None

        return key_data

    @staticmethod
    def get_currency(text):
        re_currency = regex.findall(r'\p{Sc}', text)
        if re_currency:
            currency = re_currency[0]
        else:
            logging.warning(f"no currency found at {text}")
            currency = ""

        return currency
