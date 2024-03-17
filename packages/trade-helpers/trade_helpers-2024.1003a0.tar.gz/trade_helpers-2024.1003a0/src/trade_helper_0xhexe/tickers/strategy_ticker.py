from src.trade_helper_0xhexe.type.tick_data import TickData


class StrategyTicker:
    def __init__(self, _timedelta=60):
        self.timedelta = _timedelta
        self.tick_data = []
        self.low = float("inf")
        self.high = float("-inf")
        self.open = None
        self.close = None
        self.volume = 0
        self.processed = []
        self.finalized = False

    def process(self):
        return {
            "low": self.low,
            "high": self.high,
            "open": self.open,
            "close": self.close,
            "time": self.tick_data[0].time,
            "volume": self.volume,
        }

    def tick(self, tick: TickData):
        if len(self.tick_data) == 0:
            self.open = tick.open
            self.high = tick.high
            self.low = tick.low
            self.close = tick.close
            self.volume = tick.volume
            self.tick_data.append(tick)
            self.finalized = False
            return False

        first_entry_time = self.tick_data[0].time
        last_entry_time = tick.time

        time_diff = (last_entry_time - first_entry_time).total_seconds()

        if time_diff >= self.timedelta:
            self.finalize()
            self.tick(tick)
            return True

        self.low = min(self.low, tick.low)
        self.high = max(self.high, tick.high)
        self.close = tick.close
        self.volume += tick.volume

        self.tick_data.append(tick)

        return False

    def finalize(self):
        if self.finalized:
            return
        self.close = self.tick_data[-1].close
        self.processed.append(self.process())
        self.reset()
        self.finalized = True

    def reset(self):
        self.tick_data = []
        self.low = float("inf")
        self.high = float("-inf")
        self.open = None
        self.close = None
