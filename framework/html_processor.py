import abc
import logging
from pathlib import Path

from bs4 import BeautifulSoup

logging.getLogger(__name__)


class HTMLProcessor(abc.ABC):
    """ An HTML Processor. Each processor subclass is customized to serve specific website. """

    def __init__(self, content: str = '', url: str = None):
        self.url, self.file = url, None

        if len(content.strip()) != 0:
            self.content = content
        else:
            logging.debug(f'Create HTML Processor failed with content: {content}')
            raise ValueError('No valid content or url is given for HTML Processor.')

    def from_file(self, file: Path, url: str):
        with open(file) as cache:
            self.url, self.file = url, file
            self.content = cache.read()
            logging.debug(f'Successfully read {url} cache file: {file}')

    def __repr__(self):
        if self.url is not None:
            return f'<{self.__class__.__name__} process {self.file}>'
        else:
            return f'<{self.__class__.__name__} process on HTML string>'


class ManManBuySearchResultProcessor(HTMLProcessor):
    """ An HTML Processor made for 慢慢买 search result. """
