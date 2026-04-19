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

    def __repr__(self):
        return f'<{self.__class__.__name__} work on {self._website_url}>'

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def cache_file(url: str) -> Path:
        return Path('.cache') / Path(hashlib.md5(url.encode()).hexdigest()[:12] + '.html')

    def get(self, url: str, use_cache: bool = True) -> str:
        """
        Connect to the given url, and return the string format of page source file.

        This function use cache mechanism to store recent websites' content.
        you can change the value of argument `use_cache` to control whether to use cache mechanism.
        """
        cache_path = self.cache_file(url)

        if use_cache:
            if cache_path.exists():
                # Directly load page cache.
                cache_file = open(cache_path, 'r')
                page_source = cache_file.read()
                logging.debug(f'Load {url} page source from .cache: {cache_path}')
            else:
                # Get page and store as a cache.
                page_source = self.webdriver.get(url)
                cache_file = open(cache_path, 'x')
                cache_file.write(page_source)
                logging.debug(f'Store {url} page source to file: {cache_path}')
            cache_file.close()

        else:
            page_source = self.webdriver.get(url)
        return page_source

    @abc.abstractmethod
    def search(self, keyword: str):
        pass


class ManManBuySpider(Spider):
    _website_url = 'https://www.manmanbuy.com/'
    _search_url = 'https://s.manmanbuy.com/pc/search/result?keyword={}&pageId={}'

    def search(self, keyword: str, page_limit: int = 1):
        for page in range(1, page_limit + 1):
            url = self._search_url.format(keyword, page)
            processor = ManManBuySearchResultProcessor(self.get(url), url)
            for good in processor.get_goods():
                self.data_manager.add_good(
                    GoodManager.Good(name=good.name, price=good.price, date=good.date, platform=good.platform))
