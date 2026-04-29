import unittest

from web_scraping.spider import ManManBuySpider
from web_scraping.webdriver.webdriver import FirefoxWebDriver, SafariWebDriver


class WebDriverCreateTestCase(unittest.TestCase):
    def testFirefoxInit(self):
        driver = FirefoxWebDriver()
        self.assertHasAttr(driver, 'service')
        self.assertHasAttr(driver, 'driver')
        driver.quit()

    def testSafariWebDriverInit(self):
        driver = SafariWebDriver()
        self.assertHasAttr(driver, 'service')
        self.assertHasAttr(driver, 'driver')
        driver.quit()


class WebDriverToolTestCase(unittest.TestCase):
    def testManManBuyHistoryData(self):
        spider = ManManBuySpider()
        spider.get_history_data('test_good', 'https://cu.manmanbuy.com/discuxiao_552871634.aspx')
