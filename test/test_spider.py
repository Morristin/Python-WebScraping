import unittest

from web_scraping.spider import ManManBuySpider


class SpiderInformationValidTestCase(unittest.TestCase):
    def testManManBuySpider(self):
        with ManManBuySpider() as spider:
            spider.search('A4纸')
