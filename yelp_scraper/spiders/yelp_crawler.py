import scrapy
from items import Restaurant
from scrapy.crawler import CrawlerProcess
import json
import random
import uuid


class Yelp_Crawler(scrapy.Spider):
    name = "yelp"
    allowed_domains = ["yelp.com"]
    start_urls = ["http://www.yelp.com/c/sf/restaurants"]
    COOKIES_ENABLED = False
    #download_delay = random.uniform(.25, .75)
    FEED_FORMAT = "jsonlines"

    def __init__(self, city = "San+Francisco"): 
        self.city = city
        self.filename = "crawled_data/" + city +'_'+ "items" + ".json"
        self.sortedList = []
        self.newRestaurants = []

    def parse(self, response):
        column_sets = response.selector.xpath('//ul[contains(@class, "arrange arrange--12 arrange--wrap arrange--6-units")]').xpath('.//ul[contains(@class, "ylist")]')
        for column_set in column_sets:
            urlBlock = column_set.xpath('.//li/a/@href').extract()
            for url in urlBlock:
                cuisine = url.split('/')[3]
                cuisine_url =  "http://www.yelp.com/search?find_loc=%s,+CA,+USA&start=000&cflt=%s" % (self.city,cuisine)
                yield scrapy.Request(cuisine_url,callback = self.yieldRestaurantData)


    def yieldRestaurantData(self, response):
        restaurantList = response.xpath('//li[contains(@class, "regular-search-result")]')
        pageString = response.xpath("//div[contains(@class,'page-of-pages arrange_unit arrange_unit--fill')]/text()").extract()
        print '\n' + response.url + '\n
'        for restaurant in restaurantList:
            restaurantURL = "http://www.yelp.com/" + restaurant.xpath(".//a/@href").extract()[0]
            if self.duplicateRestaurant(restaurantURL):
                continue
            request = scrapy.Request(restaurantURL,callback = self.getInfo) 
            request.meta['ID'] = str(uuid.uuid4())
            request.meta['results'] = 0
            yield request
        if  self.turnPage(pageString):
            URL = response.url.split('=')
            pageNumberIndex = URL[2].find("&")
            nextPage = URL[0] + '=' + URL[1] + '=' + str((int(URL[2][:pageNumberIndex]) + 10)) + URL[2][pageNumberIndex:] + '=' + URL[3]
            yield scrapy.Request(nextPage,self.yieldRestaurantData)

    def getInfo(self, response):
            restaurantID = response.meta['ID']
            numberofResults = response.meta['results']
            reviews = response.xpath('//div[contains(@itemprop, "review")]')
            pageString = response.xpath("//div[contains(@class,'page-of-pages arrange_unit arrange_unit--fill')]/text()").extract()
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
            if self.turnPage(pageString): 
                numberofResults = numberofResults + 20
                if (response.url).find('?') == -1:
                    nextPage = response.url + "?start=" + str(numberofResults)
                else:
                    URL = response.url.split('?')
                    nextPage =  URL[0] + '?start=' + str(numberofResults)
                request = scrapy.Request(nextPage,callback=self.getInfo)
                request.meta['ID'] = restaurantID
                request.meta['results'] = numberofResults
                yield request

    #helper class functions 

    def turnPage(self, pageString):
        try:
            pageString = pageString[0][pageString[0].find('P'):].split(" ")
            if (int(pageString[1]) < int(pageString[3])) and (int(pageString[1]) <= 30):
                return True
        except TypeError:
            print "Cuisine or Restaurant DNE"
        except IndexError:
            print "Cuisine or Restaurant DNE"
        return False


    def getHighLevelInfo(self, response):
        item = Restaurant()
        item['url'] = response.url
        item['name'] = response.xpath('//a[contains(@class, "biz-name")]//text()').extract()[0]
        item['stars'] = (response.xpath('//div[contains(@class, "rating-very-large")]//i/@title').extract_first())
        item['address'] = response.xpath('//div[contains(@class,"media-story")]/address/text()').extract()[0]
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
        first = 0
        last = len(self.sortedList)-1
        while first <= last:
            midPoint = (first + last)/2
            if self.sortedList[midPoint]["url"].find(url) >= 0:
                return True
            else:
                if url < self.sortedList[midPoint]["url"]:
                    last = midPoint -1
                else:
                    first = midPoint+1
        return False




