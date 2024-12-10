# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from fileinput import close

# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
import sqlite3


class BooksPipeline:

    def __init__(self):
        self.json_data = {}

        self.sqlite3_db = r"E:\Repositories\Python\WebCrawler\books\data\book.sqlite3"
        self.con: sqlite3.Connection = sqlite3.connect(self.sqlite3_db)

    def open_spider(self, spider: scrapy.Spider):
        pass

    def close_spider(self, spider: scrapy.Spider):
        self.con.commit()
        self.con.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        self.con.execute("INSERT INTO book (URL,Title,Price) VALUES(?,?,?)", tuple(item.values()))
        return item
