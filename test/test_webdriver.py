from framework.webdriver import FirefoxWebDriver, SafariWebDriver
import unittest


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


class WebDriverLinkTestCase(unittest.TestCase):
    def testFirefoxLink(self):
        driver = FirefoxWebDriver()
        content = driver.get('https://www.selenium.dev')
        self.assertIsNotNone(content)
        driver.quit()
