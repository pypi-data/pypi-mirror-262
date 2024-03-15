from typing import List

class Token:
    def __init__(self, name: str, address: str, decimals: int, amounts_in: List[int]):
        self.name = name
        self.address = address
        self.decimals = decimals
        self.amounts_in = amounts_in
