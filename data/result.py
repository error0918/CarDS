from dataclasses import dataclass
from typing import Optional

"""
CarDS - data.result.py
Copyright 2023. jtaeyeon05 all rights reserved
"""


@dataclass()
class Result:
    situation: Optional[str] = None
    steer: Optional[int] = None
    velocity: Optional[int] = None
