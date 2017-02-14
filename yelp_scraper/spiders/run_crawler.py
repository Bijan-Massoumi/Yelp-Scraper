from items import Restaurant
from scrapy.crawler import CrawlerProcess
import scrapy
import sys 
from cuisine_crawler import yelp_scraper
from yelp_crawler import Yelp_Crawler
from scrapy.utils.project import get_project_settings
import time



if __name__ == "__main__":
    if len(sys.argv) < 2:
        city = "Davis"
    else:
        city = sys.argv[1]
    process = CrawlerProcess(get_project_settings())
    process.crawl(Yelp_Crawler,city)
    process.start()


