from dataclasses import dataclass
from typing import List

"""
CarDS - data.data.py
Copyright 2023. jtaeyeon05 all rights reserved
"""


@dataclass()
class Data:
    second: int
    front_lidar: int
    last_steer: int
    v: List[int]
    l: List[int]
    r: List[int]
