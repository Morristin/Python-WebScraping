import abc
from typing import Generator, NamedTuple

from web_scraping.processor.data_processor import *

logging.getLogger(__name__)


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
            logging.warning(f'Create HTML Processor failed with content: {content}.')
            raise ValueError('No valid content or url is given for HTML Processor.')

    def __repr__(self):
        return f'<{self.__class__.__name__} on {self.url}>'


class ManManBuySearchResultProcessor(HTMLProcessor):
    """ An HTML Processor made for 慢慢买 search result. """

    Good = NamedTuple('Good',
                      [('name', str), ('price', int | float), ('date', dt.datetime), ('platform', str), ('link', str)])

    def get_goods(self, limit: int | None = None) -> Generator[Good]:
        goods = self.content.find_all('div', limit=limit, class_=re.compile(r'DiscountItem.*itemContent'))
        for good in goods:
            name = remove_unwanted_char(
                good.find('div', class_=re.compile(r'DiscountItem.*itemTitle')).a.attrs['title'])

            try:
                price = format_price(get_text(good.find('div', class_=re.compile(r'DiscountItem.*itemSubTitle'))))
            except InvalidDataError:
                continue

            date = format_date(get_text(good.find('span', class_=re.compile(r'DiscountItem.*itemTime'))))
            platform = get_text(good.find('span', class_=re.compile(r'DiscountItem.*itemMall')))
            link = get_link(good.find('div', class_=re.compile(r'DiscountItem.*itemTitle')))
            yield self.Good(name=name, price=price, date=date, platform=platform, link=link)
