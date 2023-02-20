from typing import Tuple
from typing import List
from typing import Optional

"""
CarDS - config.py
Copyright 2023. jtaeyeon05 all rights reserved
"""


is_canny_show = False

left_steer = -80
right_steer = 80
base_velocity = 80

A8A0, B422 = "A8A0", "B422"

difference = {
    A8A0: {
        "l": [79, 171, 261],
        "r": [72, 155, 237],
        "steer": -3
    },
    B422: {
        "l": [112, 209, 308],
        "r": [77, 162, 247],
        "steer": 13
    }
}

data_type = Tuple[
    int,  # front_lidar
    int,  # last_steer
    List[int],  # v
    List[int],  # l
    List[int],  # r
]

result_type = Tuple[
    Optional[str],  # situation
    Optional[int],  # steer
    Optional[int]  # velocity
]
