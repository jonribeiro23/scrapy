import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['https://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//table/tbody/tr")
        for country in countries:
            name = country.xpath(".//td/a/text()").get()
            debt = country.xpath(".//td[2]/text()").get()
            yield {
                'name': name,
                'debt': debt
            }
