import scrapy
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
class BatDongSanSpider(scrapy.Spider):
    name = 'alonhadat.com.vn'
    allowed_domains = ['alonhadat.com.vn']
    start_urls = ['https://alonhadat.com.vn/nha-dat/can-ban/nha-dat/2/ho-chi-minh.html']
 
    def parse(self, response):
        html_links = LinkExtractor(allow=()).extract_links(response)
        for link in html_links:
            yield response.follow(link.url, callback=self.parse)
        yield self.parse_item(response)
 
    def parse_item(self, response):
        if self._is_not_item_page(response): return
        # return { 'url_title': response.url}
        self._selenium_downloadHTML(response)
 
        code = response.url.split("-")[-1].replace(".html","")
        title = response.xpath("//*[@id='left']/div[1]/div[1]/h1/text()").get()
        descripsion = response.xpath("//*[@id='left']/div[1]/div[2]/text()").get()
        phone = self._selenium_downloadHTML(response)
        
        return {
                'url': response.url,
                'code': code,
                'title': title,
                'phone': phone,
                'description': descripsion
            }
    
    def _is_not_item_page(self, response):
        title = response.xpath("//*[@id='left']/div[1]/div[1]/h1/text()").get()
        return not title
    
    def _selenium_downloadHTML(self, response):
        options = Options()
        options.headless = True  
        driver = webdriver.Chrome(executable_path='C:/Mobifone/Crawler_Web/tutorial/chromedriver', options=options)
        driver.get(response.url)
        phone = driver.find_element_by_xpath("//*[@id='right']/div[1]/div/div[2]/div[2]/a").text
        driver.quit()
        return phone