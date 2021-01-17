import scrapy


class CrazyOffersSpider(scrapy.Spider):
    name = 'crazy_offers'
    allowed_domains = ['www.cigabuy.com']
    # start_urls = ['http://www.cigabuy.com/crazy-sales-c-56.html']
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    def start_requests(self):
        yield scrapy.Request(url='http://www.cigabuy.com/crazy-sales-c-56.html', callback=self.parse,
                             headers=self.header)

    def parse(self, response):
        for product in response.xpath("//div[@class='p_box_wrapper']"):
            name = product.xpath(".//div/a[@class='p_box_title']/text()").get()
            url = product.xpath(".//div/a[@class='p_box_title']/@href").get()
            special_price = product.xpath(".//div/div[@class='p_box_price cf']/span[@class='productSpecialPrice fl']/text()").get()
            normal_price = product.xpath(".//div/div[@class='p_box_price cf']/span[@class='normalprice fl']/text()").get()
            yield {
                'name': name,
                'normal_price': normal_price,
                'special_price': special_price,
                'url': url
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        next_page = next_page.split('/')

        if next_page:
            yield response.follow(url='/'+next_page[3], callback=self.parse, dont_filter=True, headers=self.header)
