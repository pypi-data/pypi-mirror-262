from itertools import cycle
from typing import Iterable, List

import eth_abi.abi
from eth_typing import ChecksumAddress
from eth_utils.address import to_checksum_address
from hexbytes import HexBytes
from web3 import Web3


def decode_v3_path(path: bytes) -> List[ChecksumAddress | int]:
    """
    Decode the `path` byte string used by the Uniswap V3 Router/Router2 contracts.
    `path` is a close-packed encoding of pool addresses (20 bytes) and fees
    (3 bytes).
    """

    def _extract_address(chunk: bytes) -> ChecksumAddress:
        return to_checksum_address(chunk)

    def _extract_fee(chunk: bytes) -> int:
        return int.from_bytes(chunk, byteorder="big")

    path_pos = 0
    decoded_path: List[ChecksumAddress | int] = []
    # read alternating 20 and 3 byte chunks from the encoded path,
    # store each address (hex string) and fee (int)
    for byte_length in cycle((20, 3)):
        chunk = HexBytes(path[path_pos : path_pos + byte_length])

        match byte_length:
            case 3:
                decoded_path.append(_extract_fee(chunk))
            case 20:
                decoded_path.append(_extract_address(chunk))

        path_pos += byte_length
        if path_pos == len(path):
            break

    return decoded_path


def generate_v3_pool_address(
    token_addresses: Iterable[str],
    fee: int,
    factory_address: str,
    init_hash: str,
) -> ChecksumAddress:
    """
    Generate the deterministic pool address from the token addresses and fee.

    Adapted from https://github.com/Uniswap/v3-periphery/blob/main/contracts/libraries/PoolAddress.sol
    """

    token_addresses = sorted([address.lower() for address in token_addresses])

    return to_checksum_address(
        Web3.keccak(
            HexBytes(0xFF)
            + HexBytes(factory_address)
            + Web3.keccak(
                eth_abi.abi.encode(
                    types=("address", "address", "uint24"),
                    args=(*token_addresses, fee),
                )
            )
            + HexBytes(init_hash)
        )[-20:]  # last 20 bytes of the keccak hash becomes the pool address
    )
