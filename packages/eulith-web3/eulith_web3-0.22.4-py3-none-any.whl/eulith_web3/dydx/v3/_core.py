from eth_account.messages import encode_typed_data
from eth_utils import keccak

from eulith_web3.dydx.v3._eip712 import DydxV3CreateOrderHashInput


def eip712_domain() -> dict:
    return {"name": "EulithAceDydxV3", "version": "1"}


def eip712_domain_type() -> list:
    return [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
    ]


class CreateOrderHashInputEip712:
    x: DydxV3CreateOrderHashInput

    def __init__(self, x: DydxV3CreateOrderHashInput) -> None:
        self.x = x

    @classmethod
    def eip712_type(cls) -> list:
        return [
            {"name": "market", "type": "string"},
            {"name": "side", "type": "string"},
            {"name": "orderType", "type": "string"},
            {"name": "postOnly", "type": "bool"},
            {"name": "reduceOnly", "type": "bool"},
            {"name": "size", "type": "string"},
            {"name": "price", "type": "string"},
            {"name": "limitFee", "type": "string"},
            {"name": "expiration", "type": "string"},
            {"name": "timeInForce", "type": "string"},
            {"name": "triggerPrice", "type": "string"},
            {"name": "trailingPercent", "type": "string"},
            {"name": "accountName", "type": "string"},
        ]

    @classmethod
    def eip712_type_name(cls) -> str:
        return "DydxV3CreateOrderHashInput"

    def typed_data(self) -> dict:
        types = {
            "EIP712Domain": eip712_domain_type(),
            self.eip712_type_name(): self.eip712_type(),
        }

        payload = {
            "types": types,
            "primaryType": self.eip712_type_name(),
            "domain": eip712_domain(),
            "message": {
                "market": self.x["market"],
                "side": self.x["side"],
                "orderType": self.x["order_type"],
                "postOnly": self.x["post_only"],
                "reduceOnly": self.x["reduce_only"],
                "size": self.x["size"],
                "price": self.x["price"],
                "limitFee": self.x["limit_fee"],
                "expiration": self.x["expiration"],
                "timeInForce": self.x["time_in_force"],
                "triggerPrice": self.x["trigger_price"],
                "trailingPercent": self.x["trailing_percent"],
                "accountName": self.x["account_name"],
            },
        }

        return payload

    def compute_hash(self) -> bytes:
        signable_message = encode_typed_data(full_message=self.typed_data())
        return keccak(b"\x19\x01" + signable_message.header + signable_message.body)
