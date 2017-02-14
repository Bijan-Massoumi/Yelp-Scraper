import scrapy
from scrapy.crawler import CrawlerProcess
import json
import random
import uuid
from items import Restaurant
import sys 

class yelp_scraper(scrapy.Spider):
    name = "yelp_cuisine"
    allowed_domains = ["yelp.com"]
    COOKIES_ENABLED = False
    download_delay = random.uniform(.25, .75)
    SCRAPY_SETTINGS_MODULE = "yelp_scraper.settings"


    def __init__(self, city = "San+Francisco", cuisine = "japanese"): 
        self.start_urls = ['http://www.yelp.com/search?find_loc=%s,+CA,+USA&start=000&cflt=%s' % (city, cuisine)]
        self.city = city
        self.cuisine = cuisine
        self.filename = "crawled_data/" + city +'_'+ self.cuisine[:-1] + ".json"

    def parse(self, response):
        restaurantList = response.xpath('//li[contains(@class, "regular-search-result")]')
        print '\n' + response.url + '\n'
        for restaurant in restaurantList:
            restaurantURL = "http://www.yelp.com/" + restaurant.xpath(".//a/@href").extract()[0]
            if self.duplicateRestaurant(restaurantURL):
                continue
            request = scrapy.Request(restaurantURL,callback = self.getInfo) 
            request.meta['ID'] = str(uuid.uuid4())
            yield request
        if  self.turnPage(response):
            URL = response.url.split('=')
            pageNumberIndex = URL[2].find("&")
            nextPage = URL[0] + '=' + URL[1] + '=' + str((int(URL[2][:pageNumberIndex]) + 10)) + URL[2][pageNumberIndex:] + '=' + URL[3]
            print "\n\n"
            yield scrapy.Request(nextPage,self.parse)

    def getInfo(self, response):
            restaurantID = response.meta['ID']
            reviews = response.xpath('//div[contains(@class, "review review--with-sidebar")]')
            for review in reviews:
                item = self.getHighLevelInfo(response)
                item['ID'] = restaurantID
                reviewBody = review.xpath('.//p[contains(@itemprop,"description")]/text()').extract()
                metaInfo = review.xpath('.//meta/@content').extract()
                if len(metaInfo) >= 1 and len(reviewBody) >=1:
                    item['author'] = metaInfo[0]
                    item['review_stars'] = metaInfo[1]
                    item['review_date'] = metaInfo[2] 
                    item['review_body'] = " ".join(reviewBody)
                yield item
            if self.turnPage(response): 
                if (response.url).find('=') == -1:
                    nextPage = response.url + "?start=" + '20'
                else:
                    URL = response.url.split('=')
                    nextPage =  URL[0] + '=' + str(int(URL[1])+20)
                request = scrapy.Request(nextPage,callback=self.getInfo)
                request.meta['ID'] = restaurantID
                yield request

    #helper class functions 

    def turnPage(self, response):
        pageString = response.xpath("//div[contains(@class,'page-of-pages arrange_unit arrange_unit--fill')]/text()").extract()
        pageString = pageString[0][pageString[0].find('P'):].split(" ")
        if (int(pageString[1]) < int(pageString[3])) and (int(pageString[1]) <= 30):
            return True
        return False

    def getHighLevelInfo(self, response):
        item = Restaurant()
        item['url'] = response.url
        item['name'] = response.xpath('//a[contains(@class, "biz-name")]//text()').extract()[0]
        item['stars'] = (response.xpath('//div[contains(@class, "rating-very-large")]//i/@title').extract_first())
        item['address'] = response.xpath('//address/text()').extract()[0]
        item['cuisine'] = response.xpath('//span[contains(@class, "category-str-list")]/a//text()').extract()
        item['price'] = response.xpath('//span[contains(@class, "business-attribute price-range")]/text()').extract_first()

        if  not response.xpath('//span[contains(@itemprop, "reviewCount")]//text()').extract():
            item['numberOfReviews'] = "DNE"
        else:
            item['numberOfReviews'] = response.xpath('//span[contains(@itemprop, "reviewCount")]//text()').extract()[0]

        if not response.xpath('//span[contains(@class,"neighborhood-str-list")]//text()').extract():
            item['neighborhood'] = "DNE"
        else:
            item['neighborhood'] = response.xpath('//span[contains(@class,"neighborhood-str-list")]//text()').extract()[0]    
        return item

    def duplicateRestaurant(self,url):
        with open(self.filename) as f:
            for line in f:
                if str(line).find(url) > 0:
                    return True
            return False




