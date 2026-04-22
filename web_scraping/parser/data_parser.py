import datetime as dt
import logging
import re

import bs4

from ai_integrate.ollama_integrate import Ollama
from settings.settings import settings

logging.getLogger(__name__)


class InvalidDataError(Exception):
    """ The data is marked as invalid because it's valueless for suggestion. """


def get_text(tag: bs4.element.Tag | None) -> str:
    """ Apply get_text() method on argument and handle exceptions. """
    if tag is not None:
        return tag.get_text()
    else:
        logging.warning(f'Can not perform get_text() on: {tag}')
        raise ValueError(f'Can not get information from: {tag}')


def get_title(tag, use_ai: bool = True) -> str:
    try:
        title = remove_unwanted_char(tag.a.attrs['title'])
    except AttributeError:
        logging.warning(f'Can not perform get_title() on: {tag}')
        raise ValueError(f'Can not get information from: {tag}')

    if use_ai:
        try:
            ollama = Ollama()  # TODO: 在集成更多AI模型后可能需要更改此段代码。
        except Ollama.OllamaNotEnabledError:
            pass  # Fallback to normal process.
        else:
            return ollama.chat(settings.get_text_prompt.format(tag.get_text()))

    return title


def get_link(tag) -> str:
    """ Get link from argument and handle exceptions. """
    try:
        return tag.a.attrs['href']
    except AttributeError:
        logging.warning(f'Can not perform get_link() on: {tag}')
        raise ValueError(f'Can not get information from: {tag}')


def remove_unwanted_char(text: str, unwanted_char=('\n', '，', '。', '、')):
    for char in unwanted_char:
        text = text.replace(char, ' ')
    return ' '.join(text.split())


def format_price(price: str) -> int | float:
    """
    Convert price presented in multiple ways to a single integer or float.
    """
    if re.compile(r'需.*(?:会员|VIP)').search(price) is not None:
        logging.info(f'Data is not stored as the price is invalid: {price}')
        raise InvalidDataError('The price is for member only.')
    if re.compile(r'需.*凑单').search(price) is not None:
        logging.info(f'Data is not stored as the price is useless: {price}')
        raise InvalidDataError('The price is for large-scale trade only.')

    for match in (re.compile(r'(\d+(\.\d+)?)元/件').search(price),
                  # 包含格式 "XX元拍X件(合XX元/件)" 与 "买A送A，XX元/件（共XX元）" 与 "XX元/件（共XX元）"
                  re.compile(r'(\d+(\.\d+)?)元.*实付\d+(\.\d+)?元').search(price),  # 包含格式 "XX元（买A送A实付XX元）赠送主商品"
                  re.compile(r'(\d+(\.\d+)?)元.*\d+(\.\d+)?淘?金币').search(price),  # 包含格式 "XX元+XX金币" 与 "XX元+XX淘金币"
                  ):
        if match is not None:
            break
    else:
        match = re.compile(r'(\d+(\.\d+)?)元').search(price)

    if match is not None:
        return float(match.group(1))
    else:
        logging.warning(f'Data is not stored as the price can not be recognized: {price}')
        raise InvalidDataError('The price does not match any case predefined')


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
