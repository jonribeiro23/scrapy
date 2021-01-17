import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['http://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        glasses = response.xpath(
            "//div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']")
        for glass in glasses:
            product_link = str(glass.xpath(".//div[@class='product-img-outer']/a/@href").get())
            product_name = glass.xpath(".//div[@class='p-title-block']/div[2]/div/div[1]/div/a/text()").get()
            product_price = glass.xpath(".//div[@class='p-title-block']/div[2]/div/div[2]/div/div/span/text()").get()
            meta_data = {
                'product_link': product_link,
                'product_name': product_name,
                'product_price': product_price
            }

            yield scrapy.Request(url=product_link, callback=self.parse_glasses, meta=meta_data,
                                 dont_filter=True)

        next_page = response.xpath("//li[@class='page-item']/a[@rel='next']/@href").get()

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, dont_filter=True)

    def parse_glasses(self, response):
        imgs = response.xpath(".//div[@class='swiper-container lens-pics-swiper']/div")
        for img in imgs:
            yield {
                'product_link': response.request.meta['product_link'],
                'img_link1': img.xpath(".//div[@class='swiper-slide model-image'][1]/img/@src").get(),
                'img_link2': img.xpath(".//div[@class='swiper-slide model-image'][2]/img/@src").get(),
                'product_name': response.request.meta['product_name'],
                'product_price': response.request.meta['product_price']
            }
