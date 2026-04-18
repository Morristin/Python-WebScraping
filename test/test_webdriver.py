import unittest

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
