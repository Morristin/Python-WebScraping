import unittest

from spider.spider import ManManBuySpider


class SpiderInformationValidTestCase(unittest.TestCase):
    def testManManBuySpider(self):
        # TODO: This need to be rewrite when finish writing ManManBuySpider.
        spider = ManManBuySpider()
        spider.search('纸')
        spider.stop()
