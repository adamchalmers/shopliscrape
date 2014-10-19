import scrapy
from recipe_scraper.items import RecipeItem

class RecipeSpider(scrapy.Spider):#scrapy.Spider):
    name = "taste"
    def __init__ (self, start_url):
        self.allowed_domains = ['taste.com.au']
        self.start_urls = [start_url]

    def parse(self, response):
        item = RecipeItem()
        item['name'] = response.xpath("//h1[@itemprop='name']/text()").extract()
        item['ingredients'] = response.xpath("//label[@*]/text()").extract()[:-1]
        yield item
        
