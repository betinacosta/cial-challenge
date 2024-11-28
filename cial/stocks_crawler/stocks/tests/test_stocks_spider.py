import pytest
import logging

from stocks_crawler.stocks.spiders.stocks_spider import StocksSpider
logger = logging.getLogger("StocksSpider")


@pytest.fixture
def stock_spider():
    spider = StocksSpider("aapl")
    yield spider


def test_should_return_formated_performance(stock_spider):
    performance = "2.12%"
    expected = 2.12

    assert stock_spider.format_performance(performance) == expected

def test_should_throw_error_for_missing_performance(stock_spider, caplog):
    performance_list = ["2.13%", "0.50%", "2.99%", "21.98%"]
    stock_spider.get_performances(performance_list)

    assert "information not scrapped" in caplog.records[0].msg

def test_should_return_performance_dict(stock_spider):
    performance_list = ["2.13%", "0.50%", "2.99%", "21.98%", "23.34%"]

    expected = {
        "five_days": 2.13,
        "one_month": 0.50,
        "three_months": 2.99,
        "year_to_date": 21.98,
        "one_year": 23.34
    }
    performance = stock_spider.get_performances(performance_list)

    assert expected == performance

def test_should_return_currency(stock_spider):
    text = "$3.52T"
    currency = stock_spider.get_currency(text)
    expected = "$"

    assert currency == expected

def test_should_return_empty_string_if_currency_is_missing(stock_spider, caplog):
    text = "3.52T"
    currency = stock_spider.get_currency(text)
    expected = ""

    assert currency == expected
    assert "no currency found" in caplog.records[0].msg

def test_should_return_dict_with_labels_and_values(stock_spider):
    labels = ["open", "beta", "market cap"]
    values = ["$244", "1.17", "$3.52T"]

    expected = {
        "open": "$244",
        "beta": "1.17",
        "market cap": "$3.52T"
    }
    key_data = stock_spider.get_key_data(labels, values)

    assert expected ==  key_data

def test_should_return_dict_with_none_value_if_missing(stock_spider):
    labels = ["open", "beta", "market cap"]
    values = ["$244", "1.17"]

    expected = {
        "open": "$244",
        "beta": "1.17",
        "market cap": None
    }
    key_data = stock_spider.get_key_data(labels, values)

    assert expected ==  key_data

def test_should_format_market_cap(stock_spider):
    raw_market_cap = "$3.52T"

    expected = {
        "currency": "$",
        "value": 3.52
    }
    market_cap = stock_spider.format_market_cap(raw_market_cap)
    assert market_cap == expected