import abc
import logging
import subprocess
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
        # These arguments are required to initialize by each subclass's implement.
        self.service = None
        self.driver = None

        if self.driver is not None:
            self.driver.implicitly_wait(settings.webdriver.implicitly_wait)

    def quit(self):
        self.driver.quit()

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
        super().__init__()

        self.service = webdriver.FirefoxService(executable_path=self.find_webdriver_path('geckodriver'))
        logging.debug('Successfully create firefox service.')
        self.driver = webdriver.Firefox(service=self.service)
        logging.info('Successfully create firefox web driver.')


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
