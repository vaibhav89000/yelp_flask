from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from yelpdetails.spiders.yelpfour import YelpfourSpider


process = CrawlerProcess(get_project_settings())
process.crawl(YelpfourSpider)
process.start()
