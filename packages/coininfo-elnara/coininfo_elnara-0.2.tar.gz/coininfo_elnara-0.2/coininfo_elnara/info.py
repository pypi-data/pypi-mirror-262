import requests
import unittest
from unittest.mock import patch, Mock
import time
from pprint import pprint

BASE_URL = "https://api.binance.com"


class Human:
    def __init__(self, name) -> None:
        self.name = name
        self.coins = []

    def add_coins(self):
        pass


class TickerInfo:
    @staticmethod
    def get_rolling_window_price_change(symbols: list = ["BTCUSDT"]) -> dict:
        time.sleep(3)  # 3 seconds to prevent IP address from being blocked
        if len(symbols) == 0:
            raise Exception("Symbols missing")
        if len(symbols) == 1:
            params = {"symbol": symbols}
        else:
            raise Exception("Support for more than one pair is not available")
        data = requests.get(f"{BASE_URL}/api/v3/ticker", params=params)
        if data.status_code == 200:
            result = data.json()
            return {
                "high_price": result.get("highPrice", 0),
                "low_price": result.get("lowPrice", 0),
                "open_price": result.get("openPrice", 0),
                "symbol": result.get("symbol"),
            }
        else:
            return {"message": "An error has occurred"}


class TestTickerInfo(unittest.TestCase):
    @patch("coininfo.ticker_info.requests.get")
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

    @patch("coininfo.ticker_info.requests.get")
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


if __name__ == "__main__":
    pprint(TickerInfo.get_rolling_window_price_change())
    pprint("@" * 20)
    try:
        pprint(TickerInfo.get_rolling_window_price_change(["BTCUSDT", "BNBUSDT"]))
    except Exception:
        pprint("Oopssie")
