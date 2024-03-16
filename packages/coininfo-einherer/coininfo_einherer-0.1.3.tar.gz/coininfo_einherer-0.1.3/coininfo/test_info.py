import unittest
from unittest.mock import patch, Mock
from pprint import pprint
from .info import TickerInfo
from .human import Human


class TestTickerInfo(unittest.TestCase):
    @patch("requests.get")
    @patch("time.sleep")
    def test_get_rolling_window_price_change(self, mock_sleep, mock_get):
        mock_sleep.return_value = None
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "highPrice": "0",
            "lowPrice": "0",
            "openPrice": "0",
            "symbol": "BTCUSDT",
        }
        mock_get.return_value = mock_response
        _response = TickerInfo.get_rolling_window_price_change()
        return_value = {
            "high_price": "0",
            "low_price": "0",
            "open_price": "0",
            "symbol": "BTCUSDT",
        }

        self.assertDictEqual(_response, return_value)

    @patch("requests.get")
    @patch("time.sleep")
    def test_service_down(self, mock_sleep, mock_get):
        mock_sleep.return_value = None
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        _response = TickerInfo.get_rolling_window_price_change()
        self.assertDictEqual(_response, {"message": "An error has occurred"})

    @patch("time.sleep")
    def test_when_wrong_wrong_symbols(self, mock_sleep):
        mock_sleep.return_value = None
        with self.assertRaises(Exception):
            TickerInfo.get_rolling_window_price_change([])

        with self.assertRaises(Exception):
            TickerInfo.get_rolling_window_price_change(["x", "y"])


class TestHuman(unittest.TestCase):
    def test_adding_coin(self):
        human = Human("John Doe")
        human.add_coins("BTC")  # fix bug
        human.add_coins("ETH")  # fix bug
        self.assertListEqual(human.coins, ["BTC", "ETH"])

    def test_removing_coin(self):
        human = Human("John Doe")
        human.add_coins("BTC")
        human.add_coins("ETH")
        human.remove_coin("EUR")
        human.remove_coin("BTC")
        self.assertListEqual(human.coins, ["ETH"])

    def test_display_coins(self):
        human = Human("John Doe")
        human.display_coins()
        human.add_coins("BTC")
        human.display_coins()


if __name__ == "__main__":
    pprint(TickerInfo.get_rolling_window_price_change())
    pprint("@" * 20)
    try:
        pprint(TickerInfo.get_rolling_window_price_change(["BTCUSDT", "BNBUSDT"]))
    except Exception:
        pprint("Oopssie")
