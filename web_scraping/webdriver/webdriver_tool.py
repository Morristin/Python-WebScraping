import logging

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from web_scraping.webdriver.webdriver import WebDriver

logging.getLogger(__name__)


class WebDriverTool:
    """ A toolbox offers multiple functions for specific selenium operation chains. """

    def __init__(self, webdriver: WebDriver):
        self.webdriver: WebDriver = webdriver
        self.driver = webdriver.driver

    def manmanbuy_login(self):
        wait = WebDriverWait(self.driver, timeout=20, poll_frequency=0.5, ignored_exceptions=[NoSuchElementException])
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class='pt' and contains(text(), '登录')]")))
        logging.debug(f'"登录" button is now visible on screen.')
        self.driver.find_element(By.XPATH, "//a[@class='pt' and contains(text(), '登录')]").click()

    def get_manmanbuy_history_data(self):
        """
        Get manmanbuy history data using webdriver.

        The history data of good is read from response,
        and this function require valid cookie of manmanbuy.
        """
        wait = WebDriverWait(self.driver, timeout=20, poll_frequency=0.5, ignored_exceptions=[NoSuchElementException])
        wait.until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@src, 'trendChartImage')]")))
        logging.debug(f'Trend Chart Image is now visible on screen.')
        self.driver.find_element(By.XPATH, "//img[contains(@src, 'trendChartImage')]").click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        wait.until(EC.presence_of_element_located((By.XPATH, "//canvas")))
        logging.debug(f'History Data is now presenting on screen.')
        return self.driver.execute_script('''return flotChart.oldData''')
