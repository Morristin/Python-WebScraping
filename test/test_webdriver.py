from framework.webdriver import FirefoxWebDriver
import unittest


class WebDriverCreateTestCase(unittest.TestCase):
    def testFirefoxInit(self):
        driver = FirefoxWebDriver()
        self.assertHasAttr(driver, 'service')
        self.assertHasAttr(driver, 'driver')
