import json
import logging
import os
from pathlib import Path

from selenium import webdriver

logging.getLogger(__name__)


def find_webdriver_path(webdriver_name: str) -> str | None:
    """
    Try to find where the local web driver is. **Only work with macOS and Linux**.

    If no local web driver found or system doesn't match requirement,
    return `None` to let selenium automatically download web driver.
    """
    from sys import platform
    import subprocess

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


def get_safari_driver() -> webdriver.Safari:
    class PlatformError(Exception):
        """ Try to create safari web driver on a platform which is not macOS. """

    from sys import platform
    if platform != 'darwin':
        logging.error('Try to create Safari web driver on a platform which is not macOS.')
        raise PlatformError(PlatformError.__doc__)

    service = webdriver.SafariService(executable_path=find_webdriver_path('safaridriver'))
    logging.debug('Successfully create safari service.')

    from selenium.common import SessionNotCreatedException
    try:
        driver = webdriver.Safari(service=service)
    except SessionNotCreatedException:
        print('Please execute command "safaridriver --enable" first,\n'
              'or manually toggle "Allow Remote Automation" in developer section of setting on.')
        logging.error('Failed to create safari web driver, as safari driver is not enabled yet.')
        exit()  # TODO: 可能需要更多的处理保证所有数据处于合法状态。
    else:
        logging.info('Successfully create safari web driver.')
        return driver


class Spider:
    def __init__(self):
        from settings.settings import settings

        match settings.webdriver.type:
            case "Firefox":
                service = webdriver.FirefoxService(executable_path=find_webdriver_path('geckodriver'))
                logging.debug('Successfully create firefox service.')
                self.webdriver = webdriver.Firefox(service=service)
                logging.info('Successfully create firefox web driver.')
            case "Safari":
                self.webdriver = get_safari_driver()
        self.webdriver.implicitly_wait(settings.webdriver.implicitly_wait)

    def __repr__(self):
        return f'<Spider work on {self.webdriver.__class__.__name__}>'

    def __enter__(self):
        self.webdriver.minimize_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.webdriver.quit()

    def load_cookies(self, cookies_path: str | Path, website: str = None):
        """
        Load a cookies file in JSON format for webdriver.

        Attention, **either webdriver have a tab which matches cookies,
        or a website matches cookies is given**. Else browser will raise errors.
        """
        file = Path(cookies_path) if not isinstance(cookies_path, Path) else cookies_path
        if not os.path.exists(file):
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
            self.webdriver.add_cookie(cookie)

        self.webdriver.refresh()

    def store_cookies(self, cookies_path: str | Path):
        """ Store current cookies of webdriver to a JSON file. """
        cookies = self.webdriver.get_cookies()

        if not isinstance(cookies_path, Path):
            cookies_path = Path(cookies_path)
        if not os.path.exists(cookies_path) and isinstance(cookies_path, Path):
            os.mkdir(cookies_path.parent)
            cookies_path.touch()
        with open(cookies_path, 'w') as cookies_file:
            json.dump(cookies, cookies_file)

    def get(self, url: str, use_cache: bool = False) -> str:
        """
        Connect to the given url, and return the string format of page source file.

        This function use cache mechanism to store recent websites' content.
        you can change the value of argument `use_cache` to control whether to use cache mechanism.
        """
        import hashlib
        cache_path = Path('cache') / Path(hashlib.md5(url.encode()).hexdigest()[:12] + '.html')

        if use_cache and cache_path.exists():
            # Directly load page cache.
            cache_file = open(cache_path, 'r')
            page_source = cache_file.read()
            logging.info(f'Load {url} page source from .cache: {cache_path}')
        else:
            self.webdriver.get(url)
            page_source = self.webdriver.page_source
            logging.info(f'Successfully connected to {url}.')

        if use_cache and not cache_path.exists():
            if not cache_path.parent.exists():
                os.mkdir(cache_path.parent)
            with open(cache_path, 'x') as cache_file:
                cache_file.write(page_source)
                logging.info(f'Store {url} page source to file: {cache_path}')

        return page_source
