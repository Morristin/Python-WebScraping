import abc
import json
import logging
import subprocess
from os.path import exists
from pathlib import Path
from sys import platform

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException

from settings.settings import settings

logging.getLogger(__name__)


class WebDriver(abc.ABC):
    """
    A custom webdriver, based on *selenium* project.

    Visit https://www.selenium.dev/ for more information about selenium.
    """

    @staticmethod
    def find_webdriver_path(webdriver_name: str) -> str | None:
        """
        Try to find where the local web driver is. **Only work with macOS and Linux**.

        If no local web driver found or system doesn't match requirement,
        return `None` to let selenium automatically download web driver.
        """
        if platform in ('darwin', 'linux'):
            try:
                result = subprocess.run(['which', webdriver_name], capture_output=True, timeout=1, check=True)
            except TimeoutError:
                logging.warning(f'Time out when search local web driver path: "which {webdriver_name}" time out.')
            except subprocess.CalledProcessError:
                logging.warning(f'Failed to find the local web driver: {webdriver_name}')
            else:
                if result.stdout is not None:
                    path = result.stdout.decode().strip().split('\n')[0]
                    logging.info(f'Successfully find the path of local {webdriver_name} web driver: {path}')
                    return path
                else:
                    logging.warning(f'Local web driver may not exist: {webdriver_name}')
        else:
            logging.warning(f'Current platform does not support automatically find web driver: {platform}')

        return None

    @abc.abstractmethod
    def __init__(self):
        """
        **This method should be overwritten and should not be called by subclass**.

        Because here use Firefox to activate attribute hint of IDE,
        if super().__init__() is called by subclass, a geckodriver without manager will be created.
        """
        self.service = webdriver.FirefoxService()
        self.driver = webdriver.Firefox()

    def quit(self):
        self.driver.quit()

    def load_cookies(self, filepath: str | Path, website: str = None):
        """
        Load a cookies file in JSON format for webdriver.

        Attention, **either webdriver have a tab which matches cookies,
        or a website matches cookies is given**. Else browser will raise errors.
        """
        file = Path(filepath) if not isinstance(filepath, Path) else filepath
        if not exists(file):
            logging.warning(f'Can not get cookies from cookies file: {file}')
            raise FileNotFoundError(f'Can not find cookies file: {file}')
        else:
            with open(file, 'r') as cookies_file:
                cookies = json.load(cookies_file)

        if website is not None:
            self.get(website)
        for cookie in cookies:
            if cookie["sameSite"] == "None":
                # 'secure' must be true if 'sameSite' is None
                # else the browser will refuse to load this cookie.
                cookie["secure"] = True
            self.driver.add_cookie(cookie)

        self.driver.refresh()

    def store_cookies(self, filepath: str | Path):
        """ Store current cookies of webdriver to a JSON file. """
        cookies = self.driver.get_cookies()

        if not isinstance(filepath, Path):
            filepath = Path(filepath)
        if not exists(filepath) and isinstance(filepath, Path):
            filepath.touch()
        with open(filepath, 'w') as cookies_file:
            json.dump(cookies, cookies_file)

    def get(self, url: str) -> str:
        self.driver.get(url)
        logging.info(f'Successfully connected to {url}.')
        return self.driver.page_source


class FirefoxWebDriver(WebDriver):
    """
    A webdriver whose core is provided by *geckodriver* from *mozilla*.

    Visit https://firefox-source-docs.mozilla.org/testing/geckodriver/index.html for more information.
    """

    def __init__(self):
        self.service = webdriver.FirefoxService(executable_path=self.find_webdriver_path('geckodriver'))
        logging.debug('Successfully create firefox service.')
        self.driver = webdriver.Firefox(service=self.service)
        logging.info('Successfully create firefox web driver.')

        if self.driver is not None:
            self.driver.implicitly_wait(settings.webdriver.implicitly_wait)


class SafariWebDriver(WebDriver):
    """
    A webdriver whose core is provided by *Safari* from *Apple*.

    Visit https://developer.apple.com/documentation/webkit/about-webdriver-for-safari#2957227 for more information.
    """

    class PlatformError(Exception):
        """ Try to create safari web driver on a platform which is not macOS. """

    def __init__(self):
        super().__init__()

        if platform != 'darwin':
            logging.error('Try to create Safari web driver on a platform which is not macOS.')
            raise self.PlatformError(self.PlatformError.__doc__)

        self.service = webdriver.SafariService(executable_path=self.find_webdriver_path('safaridriver'))
        logging.debug('Successfully create safari service.')
        try:
            self.driver = webdriver.Safari(service=self.service)
        except SessionNotCreatedException:
            print('Please execute command "safaridriver --enable" first,\n'
                  'or manually toggle "Allow Remote Automation" in developer section of setting on.')
            logging.error('Failed to create safari web driver, as safari driver is not enabled yet.')
            exit()  # TODO: 可能需要更多的处理保证所有数据处于合法状态。
        else:
            logging.info('Successfully create safari web driver.')

        if self.driver is not None:
            self.driver.implicitly_wait(settings.webdriver.implicitly_wait)
