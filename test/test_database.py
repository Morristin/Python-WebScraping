import unittest

from database.data_model import Good


class DataBaseTestCase(unittest.TestCase):
    def testBasicOperation(self):
        good = Good('test case')
        self.assertEqual(str(good), 'test case')

        good.add(price=42.42, date='2012-12-21', platform='Unittest')
        good += (0.01, '2000-01-01', 'Unittest')
        self.assertEqual(len(tuple(item for item in good)), 2)

        self.assertEqual(good['2012-12-21'].price, 42.42)

        good.delete('2000-01-01')
        self.assertEqual(len(tuple(item for item in good)), 1)
