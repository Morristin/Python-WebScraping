import abc
import logging
from typing import Generator, NamedTuple

import bs4

from web_scraping.processor.data_processor import *

logging.getLogger(__name__)


def get_text(tag: bs4.element.Tag | None) -> str:
    """ Apply get_text() method on argument, and format text for further operations. """
    if tag is not None:
        text = tag.get_text()
    else:
        raise ValueError('Can not get information from: {tag}')

    unwanted_char = ('\n', '，', '。', '、')
    for char in unwanted_char:
        text = text.replace(char, ' ')
    return ' '.join(text.split())


class HTMLProcessor(abc.ABC):
    """
    An HTML Processor which process given HTML file and extract information of goods.
    **The information it extracts is stored in corresponding type** for further access.

    Each subclass of processor is customized to serve specific website.
    """
    parser = 'lxml'

    def __init__(self, content: str, url: str = None):
        self.url = url

        if len(content.strip()) != 0:
            self.content = bs4.BeautifulSoup(content, self.parser)
        else:
            logging.debug(f'Create HTML Processor failed with content: {content}.')
            raise ValueError('No valid content or url is given for HTML Processor.')

    def __repr__(self):
        return f'<{self.__class__.__name__} on {self.url}>'


class ManManBuySearchResultProcessor(HTMLProcessor):
    """ An HTML Processor made for 慢慢买 search result. """

    Good = NamedTuple('Good', [('name', str), ('price', int | float), ('date', dt.datetime), ('platform', str)])

    def get_goods(self, limit: int | None = None) -> Generator[Good]:
        goods = self.content.find_all('div', limit=limit, class_=re.compile(r'DiscountItem.*itemContent'))
        for good in goods:
            name = get_text(good.find('div', class_=re.compile(r'DiscountItem.*itemTitle')))
            price = format_price(get_text(good.find('div', class_=re.compile(r'DiscountItem.*itemSubTitle'))))
            date = format_date(get_text(good.find('span', class_=re.compile(r'DiscountItem.*itemTime'))))
            platform = get_text(good.find('span', class_=re.compile(r'DiscountItem.*itemMall')))
            yield self.Good(name=name, price=price, date=date, platform=platform)
