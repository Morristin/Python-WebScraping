import datetime as dt
import os
import unittest
from pathlib import Path

from database.data_manager import GoodManager


class DatabaseOperationTestCase(unittest.TestCase):
    def testBasicOperation(self):
        path = Path('test/test_database.sqlite')
        manager = GoodManager(path)
        manager.add_good('Test Item', 9.9, dt.datetime.now(), 'Amazon', 'test-href')
        manager.add_good('中国制造设备', 8.8, dt.datetime.fromisoformat('2000-12-11 12:11'), 'WTO', 'test-href')
        manager.cursor.execute('SELECT Name FROM Goods')
        self.assertEqual(len(manager.cursor.fetchall()), 2)
        os.remove(path)
