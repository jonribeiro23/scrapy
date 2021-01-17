# -*- coding: utf-8 -*-
import scrapy


class BlusasSpider(scrapy.Spider):
    name = 'blusas'
    allowed_domains = ['www.vitrineoutlet.com.br/roupas-femininas/blusas', 'www.vitrineoutlet.com.br/roupas-femininas/blusas?p=2']
    start_urls = ['https://www.vitrineoutlet.com.br/roupas-femininas/blusas/']

    def parse(self, response):
        for product in response.xpath("//li[@class='col-sm-6 col-md-4 item last']"):

            yield{
                'title': product.xpath(".//span/h2/a/text()").get(),
                'url': product.css("span h2 a::attr(href)").extract(),
                'discounted_price': product.css("span div[class='price-box'] p span[class='price']::text").get(),
                'old_price': product.css("span div[class='price-box'] p[class='special-price'] span[class='price']::text").get()
            }

        next_page = response.xpath("//div[@class='pages text-right pagination']/ol/li[@class='current active']/following-sibling::node()/a/text()").get()
        next_page = f'https://www.vitrineoutlet.com.br/roupas-femininas/blusas?p={next_page}'

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
            })