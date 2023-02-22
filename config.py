from enum import Enum
from data.difference import *
from typing import Dict
import enum

"""
CarDS - config.py
Copyright 2023. jtaeyeon05 all rights reserved
"""


is_canny_show = False


class Cars(Enum):
    A8A0 = enum.auto()
    B422 = enum.auto()


left_steer = -80
right_steer = 80
base_velocity = 180

difference: Dict[Cars, Difference] = {
    Cars.A8A0: Difference(
        l=[79, 171, 261],
        r=[72, 155, 237],
        steer=-3
    ),
    Cars.B422: Difference(
        l=[113, 204, 295],
        r=[78, 169, 259],
        steer=8
    )
}
