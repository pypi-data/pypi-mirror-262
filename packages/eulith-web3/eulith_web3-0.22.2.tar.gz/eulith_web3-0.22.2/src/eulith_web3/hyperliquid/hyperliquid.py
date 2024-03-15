from typing import Dict, Union

from eulith_web3.hyperliquid.rpc import (
    HyperliquidGetDataRequest,
    HyperliquidTimeInForce,
)
from eulith_web3.exceptions import EulithNoSignerException
from eulith_web3.hyperliquid._eip712 import (
    HyperliquidCreateOrderHashInput,
    get_hyper_liquid_create_order_hash,
    HyperliquidCancelOrderHashInput,
    get_hyper_liquid_create_order_typed_data,
    get_hyper_liquid_cancel_order_typed_data,
    get_hyper_liquid_cancel_order_hash,
)

from eulith_web3.signing import normalize_signature


class HyperliquidClient:
    """
    A class that provides access to the GMX protocol.

    :param ew3: An instance of `EulithWeb3`.
    :type ew3: EulithWeb3
    """

    def __init__(self, ew3):
        self.ew3 = ew3

    def get_data(self, request: HyperliquidGetDataRequest) -> Dict:
        parsed_request = {
            "account_address": request.get("account_address"),
            "data_type": request.get("data_type").value,
            "ace_address": request.get("ace_address"),
        }
        return self.ew3.eulith_service.hyperliquid_get_data(parsed_request)

    def create_order(
        self,
        coin: str,
        is_buy: bool,
        size: Union[float, str],
        limit_price: Union[float, str],
        time_in_force: HyperliquidTimeInForce,
        reduce_only: bool,
        ace_address: str,
    ) -> Dict:
        try:
            self.ew3.signer.sign_msg_hash(b"")
        except AttributeError:
            raise EulithNoSignerException(
                "you must have a valid signer attached to your ew3 instance to create a hyperliquid order"
            )

        hash_input = HyperliquidCreateOrderHashInput.from_json(
            {
                "coin": coin,
                "is_buy": is_buy,
                "size": str(size),
                "limit_price": str(limit_price),
                "time_in_force": time_in_force.value,
                "reduce_only": reduce_only,
            }
        )

        typed_data = get_hyper_liquid_create_order_typed_data(hash_input)
        message_hash = get_hyper_liquid_create_order_hash(hash_input)

        signature = self.ew3.signer.sign_typed_data(typed_data, message_hash)
        signature_string = normalize_signature(signature)

        return self.ew3.eulith_service.hyperliquid_create_order(
            hash_input, signature_string, ace_address
        )

    def cancel_order(self, coin: str, oid: int, ace_address: str) -> Dict:
        try:
            self.ew3.signer.sign_msg_hash(b"")
        except AttributeError:
            raise EulithNoSignerException(
                "you must have a valid signer attached to your ew3 instance to create a hyperliquid order"
            )

        hash_input = HyperliquidCancelOrderHashInput.from_json(
            {"coin": coin, "oid": str(oid)}
        )

        typed_data = get_hyper_liquid_cancel_order_typed_data(hash_input)
        message_hash = get_hyper_liquid_cancel_order_hash(hash_input)

        signature = self.ew3.signer.sign_typed_data(typed_data, message_hash)
        signature_string = normalize_signature(signature)

        return self.ew3.eulith_service.hyperliquid_cancel_order(
            hash_input, signature_string, ace_address
        )
