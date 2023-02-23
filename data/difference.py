from dataclasses import dataclass
from typing import List

"""
CarDS - data.difference.py
Copyright 2023. jtaeyeon05 all rights reserved
"""


@dataclass()
class Difference:
    l: List[int]
    r: List[int]
    base_v: int
    steer: int
