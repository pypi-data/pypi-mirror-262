import requests
import time
from humain import Human

BASE_URL = "https://api.binance.com"


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
