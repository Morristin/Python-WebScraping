import abc
import subprocess
import logging
from sys import platform

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException

logging.getLogger(__name__)


class WebDriver(abc.ABC):
    """
    A custom webdriver, based on *selenium* project.

    Visit https://www.selenium.dev/ for more information about selenium.
    """

    class LocalWebDriverNotFoundError(Exception):
        """ Can not find where the local web driver exist. """

    @staticmethod
    def find_webdriver_path(webdriver_name) -> str:
        """ Try to find where the local web driver is. **Only work with macOS and Linux**. """
        if platform in ('darwin', 'linux'):
            try:
                subprocess_result = subprocess.run(['which', webdriver_name], capture_output=True, timeout=1,
                                                   check=True)
            except NameError:
                raise NotImplementedError(
                    'Can not call function "find_webdriver_path" without specific web driver name.')
            except TimeoutError:
                logging.debug(f'Time out when search local web driver path: "which {webdriver_name}" time out.')
                raise TimeoutError('Time out when search local web driver path.')
            except subprocess.CalledProcessError:
                logging.debug(f'Failed to find the local web driver: {webdriver_name}')
                raise WebDriver.LocalWebDriverNotFoundError()
            else:
                if subprocess_result.stdout is not None:
                    path = subprocess_result.stdout.decode().strip().split('\n')[0]
                    logging.info(f'Successfully find the path of local {webdriver_name} web driver: {path}')
                    return path
                else:
                    logging.warning(f'Local web driver may not exist: {webdriver_name}')
                    raise WebDriver.LocalWebDriverNotFoundError()
        else:
            logging.warning(f'Current platform does not support automatically find web driver: {platform}')
            raise NotImplementedError('Current platform does not support automatically find web driver.')

    @abc.abstractmethod
    def __init__(self):
        # TODO: 从本地文件当中读取全局设置
        self._implicitly_wait = 5

        # These arguments are set to None, standing for that
        # they are required to initialize by each subclass's implement.
        self.service = None
        self.driver = None

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

        # TODO: 按照设置决定是否需要优先使用本地驱动，或者将本地驱动作为在线驱动下载失败备选方案。
        self.service = webdriver.FirefoxService(executable_path=self.find_webdriver_path('geckodriver'))
        logging.debug('Successfully create firefox service.')
        self.driver = webdriver.Firefox(service=self.service)
        logging.debug('Successfully create firefox web driver.')


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
            logging.warning('Failed to create safari web driver, as safari driver is not enabled yet.')
            exit()  # TODO: 可能需要更多的处理保证所有数据处于合法状态。
        else:
            logging.debug('Successfully create safari web driver.')
