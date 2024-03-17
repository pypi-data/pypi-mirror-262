import logging


class Provider:
    def __init__(self, dry_run):
        self.dry_run = dry_run
        self.dry_run_order_id = 0
        pass

    def place_order(
        self,
        instrument_key,
        quantity=15,
        product="I",
        validity="DAY",
        price=0,
        tag=None,
        order_type="MARKET",
        transaction_type="BUY",
    ):
        raise NotImplementedError

    def place_order_dry_run(
        self,
        instrument_key,
        quantity,
        product,
        validity,
        price,
        tag,
        order_type,
        transaction_type,
    ):
        self.dry_run_order_id += 1
        logging.info(
            f"Placing dry run order {self.dry_run_order_id=} for {instrument_key=} "
            f"{quantity=} {transaction_type=} {price=} {tag=} {order_type=} {validity=} {product=}"
        )
        return f"order_{self.dry_run_order_id}"
