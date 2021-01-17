# -*- coding: utf-8 -*-
import scrapy


class GatabakanaSpider(scrapy.Spider):
    name = 'gatabakana'
    allowed_domains = ['www.gatabakana.com.br/blusas']
    start_urls = ['https://www.gatabakana.com.br/blusas/']

    def parse(self, response):
        # for product in response.xpath("//div[@class='category-products grid']/li[@class='item type-configurable']"):
        for product in response.css('li.item.type-configurable'):

            yield{
                'title': product.css("span.product-name::text").get(),
                'url': product.css("div.cont>div.imgs>a::attr(href)").extract(),
                'price': product.css("span.price::text").get()
            }

        # next_page = response.xpath("//div[@class='pages text-right pagination']/ol/li[@class='current active']/following-sibling::node()/a/@href").get()
        next_page = response.css("li.current + li > a::text").get()
        next_page = f'https://www.gatabakana.com.br/blusas?p={next_page}'

        if next_page:
            # yield scrapy.Request(url=next_page, callback=self.parse)
            yield response.follow(url=next_page, callback=self.parse)