# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from fileinput import close

# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
import json


class BooksPipeline:

    def __init__(self):
        self.json_data = {}
        self.json_file = open("data/items.json", "a", encoding='utf8')

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.json_file.close()

    def process_item(self, item, spider: scrapy.Spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
        self.json_file.write(line + '\n')
        return item
