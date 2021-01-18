import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/all/views/all/']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_path = which('chromedriver')
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://coinmarketcap.com/all/views/all/")

        # rur_tab = driver.find_element_by_xpath("//div[@class='cmc-table-listing__loadmore']")
        # rur_tab.click()

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        res = Selector(text=self.html)
        for currence in res.xpath("//tr[@class='cmc-table-row']"):
            yield {
                'name': currence.xpath(".//td[2]/div/a/text()").get(),
                'current_price': currence.xpath(".//div[@class='price___3rj7O ']/a/text()").get(),
                '24hrs': currence.xpath(".//td[8]/div/text()").get()
                }