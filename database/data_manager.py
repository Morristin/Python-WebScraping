import datetime as dt
import hashlib
import logging
import sqlite3
from pathlib import Path
from typing import NamedTuple

logging.getLogger(__name__)

Good = NamedTuple('Good', [('name', str), ('price', int | float), ('date', dt.datetime), ('platform', str)])


class GoodManager:
    """
    A manager of Good model.

    This manager make it easier for other module to access and modify data
    as they no longer need to keep data themselves.
    """

    def __init__(self):
        database_path = Path('database/goods.sqlite')
        self.database = sqlite3.connect(database_path, autocommit=True)
        self.cursor = self.database.cursor()

    def _store_good(self, good_id: str, name: str, price: int | float, date: dt.datetime, platform: str):
        """ This function store good in a safe way to prevent sqlite injection. """
        command = 'INSERT INTO Goods (ID, Name, Price, Date, Platform) VALUES (?, ?, ?, ?, ?)'
        data = (good_id, name, price, date, platform)

        try:
            self.database.execute(command, data)
        except sqlite3.OperationalError:
            self.database.execute(
                'CREATE TABLE Goods (ID varchar(32) PRIMARY KEY, Name varchar(80), Price float, Date datetime, Platform varchar(30))')
            self.database.execute(command, data)

    def add_good(self, good: Good):
        good_id = hashlib.md5((good.name + good.date.isoformat()).encode()).hexdigest()
        self._store_good(good_id, good.name, good.price, good.date, good.platform)
