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
    def find_webdriver_path(browser_name) -> str | None:
        if platform in ('darwin', 'linux'):
            try:
                subprocess_result = subprocess.run(['which', browser_name], capture_output=True, timeout=1, check=True)
            except NameError:
                raise NotImplementedError('Can not call function "find_webdriver_path" without specific browser name.')
            except TimeoutError:
                logging.warning(f'Time out when search local browser path: "which {browser_name}" time out.')
                raise TimeoutError('Time out when search local browser path.')
            except subprocess.CalledProcessError:
                logging.error(f'Failed to find the local browser: {browser_name}')
                raise WebDriver.LocalWebDriverNotFoundError()
            else:
                if subprocess_result.stdout is not None:
                    path = subprocess_result.stdout.decode().strip().split('\n')[0]
                    logging.info(f'Successfully find the path of local {browser_name} browser: {path}')
                    return path
                else:
                    logging.error(f'Local browser may not exist: {browser_name}')
                    raise WebDriver.LocalWebDriverNotFoundError()
        else:
            logging.warning(f'Current platform does not support automatically find web driver: {platform}')
            raise NotImplementedError('Current platform does not support automatically find web driver.')

    @abc.abstractmethod
    def __init__(self, /, browser_name: str, executable_path: str | None = None):
        self.browser_name = browser_name
        if executable_path is None:
            self.executable_path = WebDriver.find_webdriver_path(self.browser_name)
        else:
            self.executable_path = executable_path

    @abc.abstractmethod
    def quit(self):
        pass


class FirefoxWebDriver(WebDriver):
    """
    A custom webdriver, whose core is provided by *firefox*.

    Visit https://www.firefox.com for more information about firefox.
    """

    def __init__(self, /, browser_name: str = 'Firefox', executable_path: str | None = None):
        super().__init__(browser_name=browser_name, executable_path=executable_path)

        self.service = webdriver.FirefoxService(executable_path=self.executable_path)
        self.driver = webdriver.Firefox(service=self.service)

    def quit(self):
        self.driver.quit()
