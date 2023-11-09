from typing import List


class IPv6:
    """class name with digits"""

    def __init__(self, address: str) -> None:
        self.address: str = address


class Multicast:
    def __init__(self, address: IPv6, repetition: int):
        # List[IPv6] must be parsed
        self.addresses: List[IPv6] = [address] * repetition
