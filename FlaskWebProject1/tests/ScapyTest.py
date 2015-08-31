#import os
#os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'settings')

import unittest
from FlaskWebProject1.models.StockQuote import StockQuote as st
import sys
import time
import datetime
#import scapy
import scrapy
#from scrapy.conf import settings
from scrapy.http import Request
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.settings import CrawlerSettings, Settings

import scrapy.settings

import re
#from six.moves.urllib.parse import urlparse

import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor

from scrapy.selector import Selector
from scrapy.spider import Spider

from scrapy.item import Item, Field
class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html
        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//ul[@class="directory-url"]/li')
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('text()').re('-\s[^\n]*\\r')
            items.append(item)

        return items

class FtpSpider(scrapy.Spider):
    name = "nasdaq"
    allowed_domains = ["ftp.nasdaqtrader.com"]
    handle_httpstatus_list = [404]

    def start_requests(self):
        yield Request('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt',
                      meta={'ftp_user': 'anonymous', 'ftp_password': ''})

    def parse(self, response):
        print response.body

class TestCase(unittest.TestCase):

    def Test_Scapy(self):
        spider = FtpSpider()

        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })

        process.crawl(spider)
        process.start()

        #crawler = Crawler(settings)
        #crawler.configure()
        #crawler.crawl(spider)
        #crawler.start()
        #log.start()
        #reactor.run() # the script will block here
