from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from yelpdetails.spiders.yelptwo import YelptwoSpider


process = CrawlerProcess(get_project_settings())
process.crawl(YelptwoSpider)
process.start()
