from typing import List

from eth_account._utils.signing import to_eth_v

from eulith_web3.dydx.v3._core import CreateOrderHashInputEip712
from eulith_web3.dydx.v3._eip712 import parse_request_to_hash_input
from eulith_web3.dydx.v3.rpc import (
    DydxV3AceManagedAccount,
    DyDxV3CreateOrderParams,
    DydxV3CreateOrderResponse,
)
from eulith_web3.eulith_service import EulithService
from eulith_web3.exceptions import EulithRpcException
from eulith_web3.signer import Signer
from eulith_web3.signing import normalize_signature


class DyDxV3:
    def __init__(self, eulith_service: EulithService):
        self.eulith_service = eulith_service

    def get_ace_managed_accounts(
        self, ace_address: str
    ) -> List[DydxV3AceManagedAccount]:
        response, error = self.eulith_service.dydx_v3_get_ace_managed_accounts(
            ace_address
        )
        if error:
            raise EulithRpcException(error)
        return response

    def get_positions(self, ace_address: str, dydx_account_name: str) -> List:
        """
        :param ace_address: the ETH signing address associated with your ACE
        :param dydx_account_name: the DyDx account name you configured on your ACE
        :return: List of current positions held by the requested DyDx account
        """
        response, error = self.eulith_service.dydx_v3_get_for_account(
            ace_address, dydx_account_name, "positions"
        )
        if error:
            raise EulithRpcException(error)
        return response.get("positions")

    def get_orders(self, ace_address: str, dydx_account_name: str) -> List:
        """
        :param ace_address: the ETH signing address associated with your ACE
        :param dydx_account_name: the DyDx account name you configured on your ACE
        :return: List of current orders held by the requested DyDx account
        """
        response, error = self.eulith_service.dydx_v3_get_for_account(
            ace_address, dydx_account_name, "orders"
        )
        if error:
            raise EulithRpcException(error)
        return response.get("orders")

    def get_transfers(self, ace_address: str, dydx_account_name: str) -> List:
        """
        :param ace_address: the ETH signing address associated with your ACE
        :param dydx_account_name: the DyDx account name you configured on your ACE
        :return: List of current transfers pending in the requested DyDx account
        """
        response, error = self.eulith_service.dydx_v3_get_for_account(
            ace_address, dydx_account_name, "transfers"
        )
        if error:
            raise EulithRpcException(error)
        return response.get("transfers")

    def create_order(
        self, order: DyDxV3CreateOrderParams, ace_address: str, ace_signer: Signer
    ) -> DydxV3CreateOrderResponse:
        hash_input = parse_request_to_hash_input(order)
        hash_me = CreateOrderHashInputEip712(hash_input)
        hash_to_sign = hash_me.compute_hash()
        signature = ace_signer.sign_msg_hash(hash_to_sign)
        signature_string = normalize_signature(signature)

        response, error = self.eulith_service.dydx_v3_create_order(
            order, signature_string, ace_address
        )
        if error:
            raise EulithRpcException(error)

        return response
