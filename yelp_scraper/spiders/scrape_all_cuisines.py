import scrapy
from scrapy.crawler import CrawlerProcess
import json

class categoryCrawler(scrapy.Spider):
    name = "category"
    allowed_domains = ["yelp.com"]
    start_urls = ["http://www.yelp.com/c/sf/restaurants"]

    def parse(self,response):
        column_sets = response.selector.xpath('//ul[contains(@class, "arrange arrange--12 arrange--wrap arrange--6-units")]').xpath('.//ul[contains(@class, "ylist")]')
        file = open("all_cuisines.txt",'w')
        for column_set in column_sets:
            urlBlock = column_set.xpath('.//li/a/@href').extract()
            for url in urlBlock:
                cuisine = url.split('/')[3]
                file.write(cuisine + '\n')
                


