from unittest import TestCase
from datetime import datetime

from src.aero_svo_api import utils


class TestUtils(TestCase):

    def test_format_date(self):
        date = datetime.fromisoformat('2020-10-19T12:11:10.343138+03:00')
        formatted_date = utils.format_date(date=date)
        self.assertEqual(formatted_date, '2020-10-19T12:11:10%2B03:00')
