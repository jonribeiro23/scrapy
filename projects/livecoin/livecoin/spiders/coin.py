import scrapy


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['http://coinmarketcap.com/']

    def parse(self, response):
        pass
