from typing import List, Tuple


class IPv6:
    """class name with digits"""

    def __init__(self, address: str) -> None:
        self.address: str = address


class Multicast:
    def __init__(self, address: IPv6, repetition: int):
        # List[IPv6] must be parsed
        self.addresses: List[IPv6] = [address] * repetition

class Network:
    def __init__(self, network_devices: Tuple[IPv6, ...]):
        self.devices = network_devices
