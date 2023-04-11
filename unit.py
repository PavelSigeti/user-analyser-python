import unittest
from functions import *

class TestClass(unittest.TestCase):
    def test_ua_category(self):
        self.assertEqual(ua_category("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"), 1)
        self.assertEqual(ua_category("Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.268"), 0)

    def test_ip_info(self):
        self.assertEqual(ip_info('77.88.5.246'), [55.7386, 37.6068, 2, 0])

    def test_avg_ceil(self):
        self.assertEqual(avg_ceil([12, 20, 30, 65]), 32)

    def test_moving_avg(self):
        self.assertEqual(moving_avg([12, 20, 30, 65], 3)[1], 38.333333333333336)

if __name__=='__main__':
    unittest.main()