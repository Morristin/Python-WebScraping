import abc
import hashlib
import logging
from pathlib import Path

from database.data_manager import GoodManager
from web_scraping.processor.html_processor import ManManBuySearchResultProcessor
from web_scraping.webdriver.webdriver import FirefoxWebDriver

logging.getLogger(__name__)


class Spider(abc.ABC):
    """
    A general web_scraping model for collecting and analyzing digital trade data.
    """
    _website_url = None
    _search_url = None

    def __init__(self):
        # Check if subclass has its own valid 'website_url' and 'search_url'
        if self._website_url is None or self._search_url is None:
            raise AttributeError('Attribute "website_url" and "search_url" must be defined first in class.')

        self.webdriver = FirefoxWebDriver()  # TODO: 根据外部设置文件决定所使用的 Web Driver.
        self.data_manager = GoodManager()

    def stop(self):
        self.webdriver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Spider implement context management protocol so it can be used in `with` statement.
        When context manager exist, Spider will make sure web driver stop as expected.

        However, **Spider won't deal with any exception**, and it'll directly raise them.
        """
        self.stop()
        if exc_type is not None:
            raise exc_type(exc_val)

    def __repr__(self):
        return f'<{self.__class__.__name__} work on {self._website_url}>'

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def cache_file(url: str) -> Path:
        return Path(hashlib.md5(url.encode()).hexdigest()[:12] + '.html')

    def get(self, url: str, ignore_cache: bool = False, store_to_cache: bool = True) -> str:
        """
        Connect to the given url, and return the string format of page source file.

        This function use cache mechanism to store recent websites' content.
        If the website is dynamic, may set `ignore_cache` to True to get the newest content.
        """
        cache_filename = self.cache_file(url)
        if (Path('cache') / cache_filename).exists() and not ignore_cache:
            with open(Path('cache') / cache_filename, 'r') as cache:
                page_source = cache.read()
            logging.debug(f'Load page source from cache: {url}')
        else:
            page_source = self.webdriver.get(url)

            if store_to_cache:
                with open(Path('cache') / cache_filename, 'x') as cache:
                    cache.write(page_source)
                logging.debug(f'Successfully store page source of {url} to file: {cache_filename}')

        return page_source

    @abc.abstractmethod
    def search(self, keyword: str):
        pass


class ManManBuySpider(Spider):
    _website_url = 'https://www.manmanbuy.com/'
    _search_url = 'https://s.manmanbuy.com/pc/search/result?keyword={}'

    def search(self, keyword: str):
        url = self._search_url.format(keyword)
        processor = ManManBuySearchResultProcessor(self.get(url), url)
        for good in processor.get_goods():
            self.data_manager.add_good(good)
