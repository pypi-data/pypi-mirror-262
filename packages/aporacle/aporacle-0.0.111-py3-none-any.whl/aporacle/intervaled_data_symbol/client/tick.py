import logging

import numpy as np
import pendulum
from komoutils.core import KomoBase

from aporacle.intervaled_data_symbol.client.shared_data import SharedData
from aporacle.intervaled_data_symbol.client.trades import Trades


class Tick(KomoBase):

    def __init__(self, symbol: str, stamp: int, ttl: int = 180):
        self.symbol: str = symbol
        self.tso: str = str(symbol).split("_")[2]
        self.quote: str = str(symbol).split("_")[3]

        self.trades: list = []
        self.stamp: int = stamp
        self.ttl: int = ttl
        self.expires_at: int = self.stamp + self.ttl
        self.time: str = pendulum.from_timestamp(self.stamp).to_datetime_string()
        self.open: float = 0
        self.low: float = 0
        self.high: float = 0
        self.close: float = 0
        self.mean: float = 0
        self.volume: float = 0
        self.count: float = 0
        self.elapsed: float = 0

        self.previous_price_means: list = []
        self.previous_returns_means: dict = {"flare": [], "songbird": []}
        self.prices_smas: dict = {}
        self.returns_smas: dict = {}
        self.emas: dict = {}
        # Define window size for the moving average
        self.window_sizes = [5, 10, 15, 20, 30][0:5]

        # self.returns: float = 0
        self.returns: dict = {"flare": 0.0, "songbird": 0.0}  # {chain: return}
        self.finalized: bool = False

    @property
    def age(self):
        return pendulum.from_timestamp(self.stamp).diff(pendulum.now()).in_seconds()

    @property
    def summary(self) -> dict:
        base = {
            'base': self.tso,
            'quote': self.quote,
            'stamp': self.stamp,
            'time': self.time,
            'elapsed': self.elapsed,
            'mean_feature': round(self.mean, 8),
            'return_flare_feature': round(self.returns['flare'], 8),
            'return_songbird_feature': round(self.returns['songbird'], 8),
            'volume_feature': self.volume,
            'count': self.count,
        }

        base.update(self.prices_smas)
        base.update(self.emas)

        return base

    def initialize(self):
        # assert previous_close > 0, f"Previous close of ZERO or less encountered. {self.executor} {self.stamp}"
        previous_close = SharedData.get_instance().last_close
        previous_returns = SharedData.get_instance().last_returns
        self.mean = previous_close
        self.open = previous_close
        self.low = previous_close
        self.high = previous_close
        self.close = previous_close
        # self.returns = previous_returns
        self.volume = 1e-25
        self.count = 0
        self.elapsed = 0

    def summarize(self):
        p = [SharedData.get_instance().last_close] + [item['price'] for item in self.trades]
        prices = np.array(p)
        self.open = prices.flat[0]
        self.low = prices.min()
        self.high = prices.max()
        self.close = prices.flat[-1]
        self.mean = prices.mean()
        self.volume = np.array([item['amount'] for item in self.trades]).sum()
        self.count = len(prices)
        # print(f"Count: {self.count} Volume: {self.volume}")

    def get_prices_smas(self, index: int):
        return {f"{key}_{index}": value for key, value in self.prices_smas.items()}

    def get_returns_smas(self, chain: str, index: int):
        chain_returns: dict = self.returns_smas[chain]
        return {f"{key}_{index}": value for key, value in chain_returns.items()}

    def get_prices(self, index: int):
        return {f"{key}_{index}": value for key, value in self.summary.items() if 'feature' in key and 'mean' in key}

    def get_returns(self, chain: str, index: int):
        return {f"{key}_{index}": value for key, value in self.summary.items() if
                'feature' in key and 'return' in key and chain in key}

    def simple_moving_average(self, metric: str):
        # start_time = time.perf_counter()

        if metric == 'prices':
            # Create a numpy array from the values
            means = np.array([previous_mean for previous_mean in self.previous_price_means] + [self.mean])
            # print(f"Tick means: {means}")
            # Calculate the simple moving average
            # We use np.convolve for moving average calculation
            # 'valid' ensures that only fully overlapping sections are used
            # dividing by window_size gives the average
            for window_size in self.window_sizes:
                self.prices_smas[f"sma_{window_size}secs_{metric}_feature"] \
                    = np.convolve(means, np.ones(window_size) / window_size, mode='valid')[-1]

        elif metric == 'returns':
            for chain in ['flare', 'songbird']:
                # Create a numpy array from the values
                # print(f"Previous returns: {self.previous_returns_means}")
                # print(f"Current returns: {self.returns}")
                returns \
                    = np.array([previous_returns
                                for previous_returns in self.previous_returns_means[chain]] + [self.returns[chain]])
                # print(returns)
                _smas = {}
                for window_size in self.window_sizes:
                    _smas[f"sma_{window_size}secs_{metric}_{chain}_feature"] \
                        = np.convolve(returns, np.ones(window_size) / window_size, mode='valid')[-1]

                self.returns_smas[chain] = _smas

    def exponential_moving_average(self, weighting_factor=0.2, metric: str = 'returns'):
        # start_time = time.perf_counter()

        means = np.array([previous_mean for previous_mean in self.previous_price_means] + [self.mean])

        for period in self.window_sizes:
            ema = np.zeros(len(means))
            sma = np.mean(means[:period])
            ema[period - 1] = sma
            for i in range(period, len(means)):
                ema[i] = (means[i] * weighting_factor) + (ema[i - 1] * (1 - weighting_factor))

            self.emas[f"ema_{period}secs_{metric}_feature"] = ema.tolist()[-1]

        # end_time = time.perf_counter()

        # print(f"Time elapsed {end_time - start_time}")

    def finalize_prices(self, previous_price_means: list):
        try:
            # If there are no trades, no summaries must happen. The initialized figures stand.
            self.trades.clear()
            if self.stamp in Trades.get_instance().trades:
                self.trades = Trades.get_instance().trades[self.stamp]

            if len(self.trades) == 0:
                self.initialize()

            # print(f"Finalizing found {len(self.trades)} trades for {self.symbol} at {self.time}. ")

            # Collect previous tick means
            self.previous_price_means = previous_price_means
            # Summarize the tick trades
            self.summarize()
            self.simple_moving_average(metric='prices')

        except AssertionError as ae:
            if self.close == 0:
                self.log_with_clock(log_level=logging.WARNING,
                                    msg=f"{ae}. {self.close}. Will update with aggregated quote price when available. ")
            else:
                print(f"Error {ae}")

        except Exception as e:
            print(f"Error in finalizing {self.symbol} at {self.time}. {e}")
            raise

        self.finalized = True

    def finalize_returns(self, previous_returns_means=None):
        if previous_returns_means is None:
            previous_returns_means = {"flare": [], "songbird": []}

        try:
            # If there are no trades, no summaries must happen. The initialized figures stand.
            self.trades.clear()
            if self.stamp in Trades.get_instance().trades:
                self.trades = Trades.get_instance().trades[self.stamp]

            if len(self.trades) == 0:
                self.initialize()

            # Collect previous tick means
            self.previous_returns_means = previous_returns_means
            # calculate returns
            current_price = {}
            for chain in ['flare', 'songbird']:
                current_price[chain] = SharedData.get_instance().current_tso_prices[chain][self.tso]
                amt = (self.mean - current_price[chain]) / abs(current_price[chain])
                self.returns[chain] = amt

            self.simple_moving_average(metric='returns')

        except AssertionError as ae:
            if self.close == 0:
                self.log_with_clock(log_level=logging.WARNING,
                                    msg=f"{ae}. {self.close}. Will update with aggregated quote price when available. ")
            else:
                print(f"Error {ae}")

        except Exception as e:
            print(f"Error in finalizing {self.symbol} at {self.time}. {e}")
            raise

        self.finalized = True
