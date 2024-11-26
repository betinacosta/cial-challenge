# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StocksItem(scrapy.Item):
    five_days = scrapy.Field()
    one_month = scrapy.Field()
    three_months =  scrapy.Field()
    year_to_date = scrapy.Field()
    one_year  = scrapy.Field()
    competitors = scrapy.Field()
    market_cap = scrapy.Field()
