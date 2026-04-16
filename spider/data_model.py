from datetime import datetime


class Goods:
    """ A single good with its basic information, like name or price on specific date. """

    def __init__(self, name: str, /, price: float = None, date: str = None):
        self.name = name
        self.prices = dict()

        if date is not None and price is not None:
            self.prices[datetime.fromisoformat(date)] = price
        elif date is None and price is not None:
            self.prices[datetime.now()] = price
