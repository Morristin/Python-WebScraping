import datetime as dt
import re


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
