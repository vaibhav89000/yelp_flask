from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from yelpdetails.spiders.yelpthree import YelpthreeSpider


process = CrawlerProcess(get_project_settings())
process.crawl(YelpthreeSpider)
process.start()
