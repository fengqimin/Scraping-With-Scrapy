import scrapy
import scrapy.http
import scrapy.http.response
from books.items import BooksItem


# noinspection PyTypeChecker
class BookSpider(scrapy.Spider):
    """
    A Scrapy Spider to scrape book information from 'books.toscrape.com'.
    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): A list of domains that the spider is allowed to scrape.
        start_urls (list): A list of URLs where the spider will begin to crawl.
    Methods:
        parse(response, **kwargs):
            Parses the response from the website and extracts book information.
            Yields a BooksItem for each book found and follows pagination links.
            Args:
                response (scrapy.http.Response): The response object containing the HTML content of the page.
                **kwargs: Additional keyword arguments.
    """
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
