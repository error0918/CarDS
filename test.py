import config
from jajucha.planning import BasePlanning
from jajucha.graphics import Graphics
import sys
import keyboard

"""
CarDS - test.py
Copyright 2023. jtaeyeon05 all rights reserved 
"""


# Model
class TestPlanning(BasePlanning):
    def __init__(self, graphics_):
        super().__init__(graphics_)

    def process(
            self,
            second,
            front_image,
            rear_image,
            front_lidar,
            rear_lidar
    ):
        steer = 13
        velocity = config.base_velocity
        v, l, r = self.gridFront(front_image, cols=7, rows=3)

        if keyboard.is_pressed("+"):
            steer += 1
        elif keyboard.is_pressed("-"):
            steer -= 1

        sys.stdout.write(
            "CarDS Test\n" +
            "steer = %d\n" % steer +
            "velocity = %d\n" % velocity +
            "l[0] = %d l[1] = %d l[2] = %d | r[0] = %d r[1] = %d r[2] = %d\n"
            % (l[0], l[1], l[2], r[0], r[1], r[2]) +
            "v[0] = %d v[1] = %d v[2] = %d v[3] = %d v[4] = %d v[5] = %d\n"
            % (v[0], v[1], v[2], v[3], v[4], v[5]) +
            "\n"
        )

        return steer, velocity


# Run
graphics = Graphics(TestPlanning)
graphics.root.mainloop()
graphics.exit()
