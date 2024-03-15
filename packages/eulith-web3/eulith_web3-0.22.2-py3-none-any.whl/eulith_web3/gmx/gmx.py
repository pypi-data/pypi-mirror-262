from eulith_web3.gmx.v1.v1 import GmxV1Client
from eulith_web3.gmx.v2.v2 import GmxV2Client


class GMXClient:
    """
    A class that provides access to the GMX protocol.

    :param ew3: An instance of `EulithWeb3`.
    :type ew3: EulithWeb3

    :ivar addresses: A dictionary of GMX contract addresses.
    :vartype addresses: dict

    :ivar price_precision_decimals: The number of decimals to use for price precision.
    :vartype price_precision_decimals: int

    :ivar ew3: An instance of `EulithWeb3`.
    :vartype ew3: EulithWeb3
    """

    def __init__(self, ew3):
        self.v2 = GmxV2Client(ew3.eulith_service)
        self.v1 = GmxV1Client(ew3)
