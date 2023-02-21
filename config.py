from enum import Enum
from data.difference import *
from typing import Dict
import enum

"""
CarDS - config.py
Copyright 2023. jtaeyeon05 all rights reserved
"""


class Cars(Enum):
    A8A0 = enum.auto()
    B422 = enum.auto()


is_canny_show = False

left_steer = -80
right_steer = 80
base_velocity = 80

difference: Dict[Cars, Difference] = {
    Cars.A8A0: Difference(
        l=[79, 171, 261],
        r=[72, 155, 237],
        steer=-3
    ),
    Cars.B422: Difference(
        l=[112, 209, 308],
        r=[77, 162, 247],
        steer=13
    )
}
