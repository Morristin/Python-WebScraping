import datetime as dt
import hashlib
import logging
import sqlite3
from pathlib import Path

logging.getLogger(__name__)


class GoodManager:
    """
    A manager of Good model.

    This manager make it easier for other module to access and modify data
    as they no longer need to keep data themselves.
    """

    def __init__(self, database_path: Path = Path('database/goods.sqlite')):
        database_path.touch()  # Ensure database is existed before connect.
        self.database = sqlite3.connect(database_path, autocommit=True)
        self.cursor = self.database.cursor()

    def add_good(self, name: str, price: int | float, date: dt.datetime, platform: str = None, link: str = None):
        """
        This function store goods in a safe way to prevent sqlite injection.

        Attention, default datetime adapter of sqlite3 is deprecated as of Python 3.12,
        so this class convert `datetime` into text for easier store and read.
        """
        good_id = hashlib.md5((name + str(date.timestamp())).encode()).hexdigest()
        command = 'INSERT INTO Goods (ID, Name, Price, Date, Platform, Link) VALUES (?, ?, ?, ?, ?, ?)'
        data = (good_id, name, price, date.isoformat(sep=' '), platform, link)

        try:
            self.database.execute(command, data)
        except sqlite3.OperationalError:
            # Database has not been created yet. Directly create it.
            self.database.execute(
                'CREATE TABLE Goods (ID varchar(32) PRIMARY KEY, Name varchar(80), Price float NOT NULL, Date datetime, Platform varchar(30), Link varchar(120))')
            logging.info('Create table: Goods.')
            self.database.execute(command, data)
        except sqlite3.IntegrityError as err:
            # Goods.ID doesn't match UNIQUE requirement.
            logging.debug(f'The same good is already in database.')
            pass


data_manager = GoodManager()
