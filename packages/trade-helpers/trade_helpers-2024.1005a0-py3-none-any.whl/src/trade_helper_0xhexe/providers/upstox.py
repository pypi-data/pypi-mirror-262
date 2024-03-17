import json

from src.trade_helper_0xhexe.providers.provider import Provider
import requests


class Upstox(Provider):
    def __init__(self, dry_run, access_token):
        super().__init__(dry_run)
        self.access_token = access_token

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
        if self.dry_run:
            return self.place_order_dry_run(
                instrument_key,
                quantity,
                product,
                validity,
                price,
                tag,
                order_type,
                transaction_type,
            )

        url = "https://api.upstox.com/v2/order/place"

        payload = {
            "quantity": quantity,
            "product": product,
            "validity": validity,
            "price": price,
            "tag": tag,
            "instrument_token": instrument_key,
            "order_type": order_type,
            "transaction_type": transaction_type,
            "disclosed_quantity": 0,
            "trigger_price": 0,
            "is_amo": False,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        result = response.json()

        if result["status"] != "success":
            raise Exception("Failed to place order" + json.dumps(result))

        return result["data"]["order_id"]
