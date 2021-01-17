import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//article/h3/a'), callback='parse_item', follow=True,
             process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), follow=True,
             process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            'price': response.xpath("//div[@class='col-sm-6 product_main']/p[@class='price_color']/text()").get()
        }
