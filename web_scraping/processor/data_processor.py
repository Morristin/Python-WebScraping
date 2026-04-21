import datetime as dt
import logging
import re

import bs4

logging.getLogger(__name__)


def get_text(tag: bs4.element.Tag | None) -> str:
    """ Apply get_text() method on argument, and format text for further operations. """
    if tag is not None:
        text = tag.get_text()
    else:
        logging.warning('Can not perform get_text() on: {tag}')
        raise ValueError('Can not get information from: {tag}')
    return text


def remove_unwanted_char(text: str, unwanted_char=('\n', '，', '。', '、')):
    for char in unwanted_char:
        text = text.replace(char, ' ')
    return ' '.join(text.split())


def format_price(price: str) -> int | float:
    """
    Convert price presented in multiple ways to a single integer or float.
    """
    # TODO: 此函数目前处于占位符状态。需要进一步实现其正常功能。
    try:
        return float(re.findall(r'(\d+\.?\d*)元', price)[0])
    except IndexError:
        return float(re.findall(r'\d+', price)[0])


def format_date(date: str) -> dt.datetime:
    """
    Convert date to dt.datetime.

    First this function **check if date lack of year value** and add prefix if not.
    To simplify algorithm, it just checks whether date start with '20'.
    """
    if date[:2] != '20':
        date = f'{dt.datetime.today().year}-{date}'
    try:
        return dt.datetime.fromisoformat(date)
    except ValueError:
        raise ValueError('Argument "date" must be a iso date format string.')
