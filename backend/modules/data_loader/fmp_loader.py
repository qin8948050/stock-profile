import requests
from requests import Session

from modules.data_loader.base import DataLoader
from core.config import AppConfig


class FMPBaseLoader:
    """
    Base loader for Financial Modeling Prep API.
    Manages API connection and data fetching logic.
    """
    BASE_URL = "https://financialmodelingprep.com/api/v3" # 使用 v3 API 更常见

    def __init__(self, apikey: str):
        if not apikey:
            raise ValueError("API key cannot be empty.")
        self._apikey = apikey
        self._session = requests.Session() # 使用 Session 提高性能

    def fetch_json(self, endpoint: str, symbol: str):
        """
        Fetches data from a given FMP endpoint.
        """
        params = {"symbol": symbol, "apikey": self._apikey}
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            resp = self._session.get(url, params=params)
            resp.raise_for_status()
            data_list = resp.json()
        except requests.exceptions.RequestException as e:
            # 考虑加入日志记录
            print(f"Error fetching data for {symbol} from {endpoint}: {e}")
            return None
        except requests.exceptions.JSONDecodeError:
            # API 可能返回了非 JSON 的错误页面
            print(f"Failed to decode JSON for {symbol} from {endpoint}.")
            return None

        if not data_list:
            return None

        # 默认返回列表的第一个元素（通常是最新一期）
        return data_list[0]


class FMPBalanceSheetLoader(DataLoader):
    """Loads balance sheet data using FMPBaseLoader."""
    def __init__(self, config: AppConfig):
        self.fmp_loader = FMPBaseLoader(apikey=config.financial_modeling_prep.apikey)

    def load(self, company_code: str):
        return self.fmp_loader.fetch_json("balance-sheet-statement", company_code)
