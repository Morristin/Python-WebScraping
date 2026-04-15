import abc
import subprocess
import logging
from sys import platform

from selenium import webdriver


class WebDriver(abc.ABC):
    """
    A custom webdriver, based on *selenium* project.

    Visit https://www.selenium.dev/ for more information about selenium.
    """

    class LocalWebDriverNotFoundError(Exception):
        """ Can not find where the local web driver exist. """

    @staticmethod
    def find_webdriver_path(webdriver_name) -> str | None:
        """ Try to find where the local web driver is. **Only work with macOS and Linux**. """
        if platform in ('darwin', 'linux'):
            try:
                subprocess_result = subprocess.run(['which', webdriver_name], capture_output=True, timeout=1,
                                                   check=True)
            except NameError:
                raise NotImplementedError(
                    'Can not call function "find_webdriver_path" without specific web driver name.')
            except TimeoutError:
                logging.warning(f'Time out when search local web driver path: "which {webdriver_name}" time out.')
                raise TimeoutError('Time out when search local web driver path.')
            except subprocess.CalledProcessError:
                logging.error(f'Failed to find the local web driver: {webdriver_name}')
                raise WebDriver.LocalWebDriverNotFoundError()
            else:
                if subprocess_result.stdout is not None:
                    path = subprocess_result.stdout.decode().strip().split('\n')[0]
                    logging.info(f'Successfully find the path of local {webdriver_name} web driver: {path}')
                    return path
                else:
                    logging.error(f'Local web driver may not exist: {webdriver_name}')
                    raise WebDriver.LocalWebDriverNotFoundError()
        else:
            logging.warning(f'Current platform does not support automatically find web driver: {platform}')
            raise NotImplementedError('Current platform does not support automatically find web driver.')

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def quit(self):
        pass


class FirefoxWebDriver(WebDriver):
    """
    A custom webdriver, whose core is provided by *geckodriver* from *mozilla*.

    Visit https://firefox-source-docs.mozilla.org/testing/geckodriver/index.html for more information.
    """

    def __init__(self):
        # TODO: 按照设置决定是否需要优先使用本地驱动，或者将本地驱动作为在线驱动下载失败备选方案。
        self.service = webdriver.FirefoxService(executable_path=self.find_webdriver_path('geckodriver'))
        self.driver = webdriver.Firefox(service=self.service)

    def quit(self):
        self.driver.quit()
