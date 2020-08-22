from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from yelpdetails.spiders.yelp import YelpSpider


process = CrawlerProcess(get_project_settings())
process.crawl(YelpSpider)
process.start()
