import numpy as np

from src.trade_helper_0xhexe.tickers.strategy_ticker import StrategyTicker


class BollingerBands(StrategyTicker):
    def __init__(self, period=20, num_std=2, _timedelta=60, key="close"):
        super().__init__(_timedelta)
        self.period = period
        self.num_std = num_std
        self.key = key

    def process(self):
        if len(self.processed) < self.period:
            return super().process()

        closes = np.array([data[self.key] for data in self.processed[-self.period:]])
        sma = np.mean(closes)
        std_dev = np.std(closes)

        upper_band = sma + (self.num_std * std_dev)
        lower_band = sma - (self.num_std * std_dev)

        return {
            'low': self.low,
            'high': self.high,
            'open': self.open,
            'close': self.close,
            'time': self.tick_data[0].time,
            'sma': sma,
            'upper_band': upper_band,
            'lower_band': lower_band
        }
