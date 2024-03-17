from src.trade_helper_0xhexe.providers.upstox import Upstox


def test_provider():
    upstox = Upstox(dry_run=True, access_token="access_token")

    order_id = upstox.place_order(
        instrument_key="instrument_key",
        quantity=15,
        product="I",
        validity="DAY",
        price=0,
        tag=None,
        order_type="MARKET",
        transaction_type="BUY",
    )

    assert order_id == "order_1"
