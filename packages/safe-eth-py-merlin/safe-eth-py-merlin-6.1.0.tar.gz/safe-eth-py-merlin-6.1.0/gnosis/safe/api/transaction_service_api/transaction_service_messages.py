import time
from typing import Dict

from eth_typing import ChecksumAddress


def get_totp() -> int:
    """

    :return: time-based one-time password
    """
    return int(time.time()) // 3600


def get_delegate_message(cls, delegate_address: ChecksumAddress) -> str:
    """
    Retrieves the required message for creating or removing a delegate on Safe Transaction Service.

    :param cls:
    :param delegate_address:
    :return: generated str message
    """
    totp = get_totp()
    return delegate_address + str(totp)


def get_remove_transaction_message(
    safe_address: ChecksumAddress, safe_tx_hash: bytes, chain_id: int
) -> Dict:
    """
    Retrieves the required message for removing a not executed transaction on Safe Transaction Service.

    :param safe_address:
    :param safe_tx_hash:
    :param chain_id:
    :return: generated EIP712 message
    """
    remove_transaction_message = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "DeleteRequest": [
                {"name": "safeTxHash", "type": "bytes32"},
                {"name": "totp", "type": "uint256"},
            ],
        },
        "primaryType": "DeleteRequest",
        "domain": {
            "name": "Safe Transaction Service",
            "version": "1.0",
            "chainId": chain_id,
            "verifyingContract": safe_address,
        },
        "message": {
            "safeTxHash": safe_tx_hash,
            "totp": get_totp(),
        },
    }
    return remove_transaction_message
