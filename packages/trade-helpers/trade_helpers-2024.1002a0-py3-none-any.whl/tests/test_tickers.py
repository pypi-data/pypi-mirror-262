from datetime import datetime

from src.trade_helper_0xhexe import HeikinAshi
from src.trade_helper_0xhexe import StrategyTicker
from src.trade_helper_0xhexe.type.tick_data import TickData


def test_tickers():
    ticker = StrategyTicker()

    tick = TickData(low=100, high=200, _open=150, close=180, time=1710474320, volume=1)
    ticker.tick(tick)
    assert ticker.low == 100
    assert len(ticker.tick_data) == 1
    assert len(ticker.processed) == 0

    tick = TickData(low=100, high=200, _open=150, close=180, time=1710474516)
    ticker.tick(tick)

    assert len(ticker.tick_data) == 1
    assert len(ticker.processed) == 1

    tick = TickData(low=100, high=260, _open=150, close=120, time=1710474517)
    ticker.tick(tick)

    assert len(ticker.tick_data) == 2
    assert len(ticker.processed) == 1

    tick = TickData(low=100, high=200, _open=150, close=120, time=1710474617)
    ticker.tick(tick)

    assert len(ticker.tick_data) == 1
    assert len(ticker.processed) == 2

    ticker.finalize()

    assert len(ticker.tick_data) == 0
    assert len(ticker.processed) == 3


def test_ha():
    ticker = HeikinAshi()

    # Create a series of TickData objects
    ticks = [
        TickData(
            low=100,
            high=200,
            _open=150,
            close=180,
            time=datetime(2023, 1, 1, 9, 30),
            volume=100,
        ),
        TickData(
            low=120,
            high=220,
            _open=170,
            close=200,
            time=datetime(2023, 1, 1, 9, 31),
            volume=200,
        ),
        TickData(
            low=140,
            high=240,
            _open=190,
            close=220,
            time=datetime(2023, 1, 1, 9, 32),
            volume=300,
        ),
        TickData(
            low=160,
            high=260,
            _open=210,
            close=240,
            time=datetime(2023, 1, 1, 9, 33),
            volume=400,
        ),
        TickData(
            low=180,
            high=280,
            _open=230,
            close=260,
            time=datetime(2023, 1, 1, 9, 34),
            volume=500,
        ),
    ]

    # Process the ticks
    for tick in ticks:
        ticker.tick(tick)

    # Finalize the last tick
    ticker.finalize()

    # Check the processed Heikin-Ashi data
    assert len(ticker.processed) == len(ticks)

    for i, processed_data in enumerate(ticker.processed):
        assert processed_data["low"] == ticks[i].low
        assert processed_data["high"] == ticks[i].high
        assert processed_data["open"] == ticks[i].open
        assert processed_data["close"] == ticks[i].close
        assert processed_data["time"] == ticks[i].time
        assert processed_data["volume"] == ticks[i].volume

        if i == 0:
            assert processed_data["ha_open"] == ticks[i].open
            assert processed_data["ha_close"] == ticks[i].close
            assert processed_data["ha_high"] == ticks[i].high
            assert processed_data["ha_low"] == ticks[i].low
        else:
            prev_ha_open = ticker.processed[i - 1]["ha_open"]
            prev_ha_close = ticker.processed[i - 1]["ha_close"]

            ha_close = (
                ticks[i].open + ticks[i].high + ticks[i].low + ticks[i].close
            ) / 4
            ha_open = (prev_ha_open + prev_ha_close) / 2
            ha_high = max(ticks[i].high, ha_open, ha_close)
            ha_low = min(ticks[i].low, ha_open, ha_close)

            assert processed_data["ha_open"] == ha_open
            assert processed_data["ha_close"] == ha_close
            assert processed_data["ha_high"] == ha_high
            assert processed_data["ha_low"] == ha_low

        assert (
            processed_data["color"] == "green"
            if processed_data["ha_open"] < processed_data["ha_close"]
            else "red"
        )

    print("All tests passed!")
