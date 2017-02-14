# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

class JsonWriterPipeline(object):
        
    def open_spider(self,spider):
        self.file = open(spider.filename, 'a')
        self.file.close()
        with open(spider.filename) as f:
            for line in f:
                spider.sortedList.append(json.loads(line))

    def process_item(self, item, spider):
        spider.newRestaurants.append(item)
        return item

    def close_spider(self,spider):
        spider.sortedList = spider.sortedList + spider.newRestaurants
        spider.sortedList = sorted(spider.sortedList, key=lambda k: k['url'])
        self.file = open(spider.filename, 'wb')
        for item in spider.sortedList:
            try:
                item["author"] = item["author"]
                line = json.dumps(dict(item)) + "\n"
                self.file.write(line)
            except Exception as e:
                continue
