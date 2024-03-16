from enum import Enum
from typing import TypedDict

from eulith_web3.hyperliquid._eip712 import (
    HyperliquidCreateOrderHashInput,
    HyperliquidCancelOrderHashInput,
)


class HyperliquidDataType(Enum):
    META_INFO = "meta_info"
    MID_PRICES = "mid_prices"
    ASSET_CONTEXTS = "asset_contexts"
    OPEN_ORDERS = "open_orders"
    USER_STATE = "user_state"
    USER_FILLS = "user_fills"


class HyperliquidTimeInForce(Enum):
    GOOD_TIL_CANCEL = "Gtc"


class HyperliquidGetDataRequest(TypedDict):
    account_address: str
    data_type: HyperliquidDataType
    ace_address: str


class HyperliquidCreateOrderRequest(TypedDict):
    ace_address: str
    signature: str
    order: HyperliquidCreateOrderHashInput


class HyperliquidCancelOrderRequest(TypedDict):
    ace_address: str
    signature: str
    order: HyperliquidCancelOrderHashInput
