import scrapy
import scrapy.http
import scrapy.http.response
from books.items import BooksItem


# noinspection PyTypeChecker
class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response: scrapy.http.Response, **kwargs):
        for book in response.css(
                "article.product_pod",
        ):  # type ignore
            item = BooksItem()
            item["url"] = response.urljoin(book.css("h3 > a::attr(href)").get())
            item["title"] = book.css("h3 > a::attr(title)").get()
            item["price"] = book.css(".price_color::text").get()
            yield item

        next_page = response.css("li.next>a::attr(href)").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            # print(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
