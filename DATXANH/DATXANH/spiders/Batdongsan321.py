import scrapy
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

# rm batdongsan321.jl; scrapy crawl batdongsan321.com -o batdongsan321.jl
class BatDongSanSpider(scrapy.Spider):
    name = 'batdongsan321.com'
    allowed_domains = ['batdongsan321.com']
    start_urls = ['https://batdongsan321.com/nha-dat-ban/ho-chi-minh#/']
 
    def parse(self, response):
        html_links = LinkExtractor(allow=('/nha-dat/','/nha-dat-ban-nha/', '/nha-dat-cho-thue/', '/nha-dat-ban/')).extract_links(response)
        for link in html_links:
            yield response.follow(link.url, callback=self.parse)
        yield self.parse_item(response)
 
    def parse_item(self, response):
        if self._is_not_item_page(response): return
 
        code = response.xpath("//*[@id='main']/div[1]/div/section[1]/div[2]/div[6]/div/ul/li[3]/span[2]/text()").get()
        title = response.xpath("//*[@id='main']/div[1]/div/section[1]/h1/text()").get()
        descripsion = response.xpath("//*[@id='Form1']/div[4]/div[1]/div/div[1]/div[1]//text()").getall()
        phone = self._selenium_getphone(response)
        
        return {
                'url': response.url,
                'code': code,
                'title': title,
                'description': " ".join(descripsion).replace("\r"," ").replace("\n","").replace("\t","").strip(),
                'phone':  phone
            }
    
    def _is_not_item_page(self, response):
        title = response.xpath("//*[@id='main']/div[1]/div/section[1]/h1/text()").get()
        return not title
 
    def _selenium_getphone(self, response):
        options = Options()
        options.headless = True  
        driver = webdriver.Chrome(executable_path='C:/Mobifone/Crawler_Web/tutorial/chromedriver', options=options)
        driver.get(response.url)
 
        phone_button = driver.find_element_by_xpath("//*[@id='main']/div[1]/div/section[1]/div[2]/div[4]/div/span/span/a/button")
        phone_button.click()
        time.sleep(2)
        now = datetime.now()
        phone = driver.find_element_by_xpath("//*[@id='main']/div[1]/div/section[1]/div[2]/div[4]/div/span/span/a").text
        while "*" in str(phone):
            phone = driver.find_element_by_xpath("//*[@id='main']/div[1]/div/section[1]/div[2]/div[4]/div/span/span/a").text
            if (datetime.now() - now).total_seconds() > 10: break
        driver.quit()
        return phone