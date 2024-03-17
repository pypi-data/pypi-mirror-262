from src.trade_helper_0xhexe.tickers.strategy_ticker import StrategyTicker


class HeikinAshi(StrategyTicker):
    def process(self):
        if len(self.processed) < 1:
            ha_open = self.open
            ha_close = self.close
            ha_high = self.high
            ha_low = self.low
        else:
            prev_ha_open = self.processed[-1]["ha_open"]
            prev_ha_close = self.processed[-1]["ha_close"]

            ha_close = (self.open + self.high + self.low + self.close) / 4
            ha_open = (prev_ha_open + prev_ha_close) / 2
            ha_high = max(self.high, ha_open, ha_close)
            ha_low = min(self.low, ha_open, ha_close)

        return {
            "low": self.low,
            "high": self.high,
            "open": self.open,
            "close": self.close,
            "time": self.tick_data[0].time,
            "volume": self.volume,
            "ha_open": ha_open,
            "ha_close": ha_close,
            "ha_high": ha_high,
            "ha_low": ha_low,
            "color": "green" if ha_open < ha_close else "red",
        }
