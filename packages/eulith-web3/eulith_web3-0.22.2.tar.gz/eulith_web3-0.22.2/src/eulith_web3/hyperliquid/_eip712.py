from dataclasses import dataclass

from eth_account.messages import encode_typed_data
from eth_utils import keccak


@dataclass
class HyperliquidCreateOrderHashInput:
    coin: str
    is_buy: bool
    size: str
    limit_price: str
    time_in_force: str
    reduce_only: bool

    @classmethod
    def from_json(cls, data: dict) -> "HyperliquidCreateOrderHashInput":
        return cls(
            coin=data["coin"],
            is_buy=data["is_buy"],
            size=data["size"],
            limit_price=data["limit_price"],
            time_in_force=data["time_in_force"],
            reduce_only=data["reduce_only"],
        )

    def to_json(self) -> dict:
        return dict(
            coin=self.coin,
            is_buy=self.is_buy,
            size=self.size,
            limit_price=self.limit_price,
            time_in_force=self.time_in_force,
            reduce_only=self.reduce_only,
        )


def get_hyper_liquid_create_order_typed_data(
    message: HyperliquidCreateOrderHashInput,
) -> dict:
    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
        ],
        "HyperliquidCreateOrderHashInput": [
            {"name": "coin", "type": "string"},
            {"name": "isBuy", "type": "bool"},
            {"name": "size", "type": "string"},
            {"name": "limitPrice", "type": "string"},
            {"name": "timeInForce", "type": "string"},
            {"name": "reduceOnly", "type": "bool"},
        ],
    }

    payload = {
        "types": types,
        "primaryType": "HyperliquidCreateOrderHashInput",
        "domain": {"name": "EulithAceHyperliquid", "version": "1"},
        "message": {
            "coin": message.coin,
            "isBuy": message.is_buy,
            "size": message.size,
            "limitPrice": message.limit_price,
            "timeInForce": message.time_in_force,
            "reduceOnly": message.reduce_only,
        },
    }

    return payload


def get_hyper_liquid_create_order_hash(
    message: HyperliquidCreateOrderHashInput,
) -> bytes:
    signable_message = encode_typed_data(
        full_message=get_hyper_liquid_create_order_typed_data(message)
    )
    return keccak(b"\x19\x01" + signable_message.header + signable_message.body)


@dataclass
class HyperliquidCancelOrderHashInput:
    coin: str
    oid: str

    @classmethod
    def from_json(cls, data: dict) -> "HyperliquidCancelOrderHashInput":
        return cls(coin=data["coin"], oid=data["oid"])

    def to_json(self) -> dict:
        return dict(coin=self.coin, oid=self.oid)


def get_hyper_liquid_cancel_order_typed_data(
    message: HyperliquidCancelOrderHashInput,
) -> dict:
    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
        ],
        "HyperliquidCancelOrderHashInput": [
            {"name": "coin", "type": "string"},
            {"name": "oid", "type": "string"},
        ],
    }

    payload = {
        "types": types,
        "primaryType": "HyperliquidCancelOrderHashInput",
        "domain": {"name": "EulithAceHyperliquid", "version": "1"},
        "message": {"coin": message.coin, "oid": message.oid},
    }

    return payload


def get_hyper_liquid_cancel_order_hash(
    message: HyperliquidCancelOrderHashInput,
) -> bytes:
    signable_message = encode_typed_data(
        full_message=get_hyper_liquid_cancel_order_typed_data(message)
    )
    return keccak(b"\x19\x01" + signable_message.header + signable_message.body)
