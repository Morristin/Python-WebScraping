import logging
import datetime as dt
from typing import NamedTuple, Iterable

logging.getLogger(__name__)


class Good:
    """ A single good with its basic information, like name or price on specific date. """
    Price = NamedTuple('Price', [('price', float), ('date', dt.date), ('platform', str | None)])

    def __init__(self, name: str):
        self.name, self.prices = name, list()

    def __repr__(self):
        return f'<Good {self.name} with {len(self.prices)} price data>'

    def __str__(self):
        return self.name

    def __getitem__(self, date: str | dt.date) -> Price:
        """ Get the price on specific date. Date must be a string or datetime.date. """
        try:
            index = self.format_date(date)
        except ValueError:
            raise KeyError(f'Only "str" and "datetime.date" can be used as key, not {type(date)}.')

        for item in self.prices:
            if item.date == index:
                logging.debug(f'Successfully get price on {date}: {item}')
                return item
        else:
            logging.debug(f'Failed to get price on {date}: no data is found')
            raise KeyError(f'No price is found on {date}.')

    def __iter__(self):
        prices = sorted(self.prices, key=lambda price: price.date)
        return iter(prices)

    @staticmethod
    def format_date(date) -> dt.date:
        if not isinstance(date, dt.date):
            try:
                date = dt.date.fromisoformat(date)
            except ValueError:
                raise ValueError('Argument "date" must be a iso date format string.')
        return date

    def add(self, price: int | float, date: str | dt.date = None, platform: str = None):
        if not isinstance(price, (int, float)):
            raise ValueError('Price must be an integer or a float.')

        if date is not None and price is not None:
            self.prices.append(self.Price(price=price, date=self.format_date(date), platform=platform))
            logging.debug(f'Successfully store price on {self.format_date(date)} for {self.name}: {price}')
        elif date is None and price is not None:
            self.prices.append(self.Price(price=price, date=dt.date.today(), platform=platform))
            logging.debug(f'Successfully store price on {date} for {self.name}: {price}')

    def __iadd__(self, other: Iterable):
        if not isinstance(other, Iterable):
            raise TypeError(f'unsupported operand type(s) for +: "Good" and "{type(other)}"')
        try:
            self.add(*other)
        except TypeError:
            raise TypeError(f'{other} can not be used for + because it has too many elements.')
        else:
            return self

    def delete(self, date: str | dt.date):
        try:
            delete_item = self[date]
        except KeyError:
            raise KeyError(f'Can not perform deleting as no data found on {date}')
        else:
            self.prices.remove(delete_item)
