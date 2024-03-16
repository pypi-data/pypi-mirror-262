import logging
import os

import requests
from komoutils.core.time import the_time_in_iso_now_is

from aporacle.intervaled_data_symbol.execution.executor import IntervaledTradingSymbolExecutor

if "TSO_SETUP_URL" not in os.environ:
    raise Exception("TSO_SETUP_URL value MUST be set. ")

logging.basicConfig(level=logging.INFO)

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)


def log_with_clock(log_level: int, msg: str, **kwargs):
    app_logger.log(log_level, f"{msg} [clock={str(the_time_in_iso_now_is())}]", **kwargs)


# def get_api_setup_data():
#     url = f"http://{os.getenv('TSO_SETUP_URL')}/setup"
#
#     try:
#         with requests.Session() as session:
#             response = session.get(url=url)
#             response.raise_for_status()
#             setup = response.json()
#             return setup
#
#     except requests.exceptions.HTTPError as e:
#         app_logger.error(f"Please ensure that {url} is valid")
#     except requests.exceptions.ConnectionError as e:
#         raise SetupResourceNotAvailableException()
#     except Exception as e:
#         raise SetupResourceNotAvailableException(f"Undocumented asset setup acquisition error - {e}")


class SetupResourceNotAvailableException(Exception):
    """Exception raised when a connection error happens while accessing TSO_SETUP.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message: str = "TSO Setup not available. "):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class ConversionRateResourceNotAvailableException(Exception):
    """Exception raised when a connection error happens while accessing TSO_SETUP.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message: str = "Conversion rate resource error. "):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class SymbolNotFoundException(Exception):
    def __init__(self, symbol: str):
        self.symbol = symbol


class SymbolHasNoRateException(Exception):
    def __init__(self, symbol: str):
        self.symbol = symbol


__all__ = [
    "IntervaledTradingSymbolExecutor"
]
