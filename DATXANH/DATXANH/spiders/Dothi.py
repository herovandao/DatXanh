import scrapy
from scrapy.linkextractors import LinkExtractor

# rm dothi.jl; scrapy crawl dothi.net -o dothi.jl 
class DothiSpider(scrapy.Spider):
    name = 'dothi.net'
    allowed_domains = ['dothi.net']
    start_urls = ['https://dothi.net/nha-dat-ban-tp-hcm.htm']
 
    def parse(self, response):
        html_links = LinkExtractor(allow=()).extract_links(response)

        a_tags = response.xpath("//*[@id='Form1']/div[4]/div[1]/div/div[1]//li//a/@href").getall()
        for a in a_tags:
            yield response.follow('https://dothi.net'+a, callback=self.parse) 

        for link in html_links:
            yield response.follow(link.url, callback=self.parse)
        yield self.parse_item(response)
    
    def parse_item(self, response):
        if self._is_not_item_page(response): return
 
        code = response.xpath("//*[@id='tbl1']/tbody/tr[1]/td[2]/text()").get()
        title = response.xpath("//*[@id='Form1']/div[4]/div[1]/div/div[1]/div[1]/h1/text()").get()
        descripsion = response.xpath("//*[@id='Form1']/div[4]/div[1]/div/div[1]/div[1]//text()").getall()
        phone = response.xpath("//*[@id='tbl2']//tr[4]//td/text()").get()
        
        return {
                'url': response.url,
                'code': str(code).replace("\r","").replace("\n",""),
                'title': str(title).replace("\r","").replace("\n",""),
                'description': " ".join(descripsion).replace("\r"," ").replace("\n","").replace("\t","").strip(),
                'phone': str(phone).replace("\r","").replace("\n","")
            }
    
    def _is_not_item_page(self, response):
        title = response.xpath("//*[@id='Form1']/div[4]/div[1]/div/div[1]/div[1]/h1/text()").get()
        return not title
