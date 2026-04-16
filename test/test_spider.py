import unittest

from spider.spider import ManManBuySpider


class SpiderInformationValidTestCase(unittest.TestCase):
    def testManManBuySpider(self):
        spider = ManManBuySpider()
        spider.search('纸')
        spider.stop()
