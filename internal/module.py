import sys
from enum import Enum
from data.data import *
from data.difference import *
from data.result import *
# from internal import halt
from internal import util
from internal import module
from typing import List
from typing import Tuple
import config
import keyboard

"""
CarDS - internal.module.py
Copyright 2023. jtaeyeon05 all rights reserved
"""

hold_frame: Tuple[bool, int] = (False, 0)
last_result: Result = Result()


class Direction(Enum):
    Straight = 1
    Left = 2
    Right = 3
    Stop = 4


def operation(
        result_list: List[Result]
) -> Result:
    result = Result()
    for op_result in result_list:
        if op_result is not None:
            result = Result(
                situation=util.not_none(op_result.situation, result.situation),
                steer=util.not_none(op_result.steer, result.steer),
                velocity=util.not_none(op_result.velocity, result.velocity)
            )
    return result


def default(
        data: Data, difference_data: Difference
) -> Result:
    return operation(
        result_list=[
            velocity(data=data),
            steer(data=data, difference_data=difference_data),
            curve(data=data, difference_data=difference_data),
            left_right_angle(data=data),
            # right_right_angle(data=data)
        ]
    )


def velocity(
        data: Data
) -> Result:
    situation = "직진"
    if data.v[0] < data.v[1] < data.v[2] < data.v[3] \
            and data.v[3] > data.v[4] > data.v[5] > data.v[6] \
            and -10 < 2 * data.v[5] - (data.v[4] + data.v[6]) < 10 \
            and -10 < 2 * data.v[1] - (data.v[0] + data.v[2]) < 10 \
            and data.v[3] > 170:
        return Result(situation=situation, velocity=config.base_velocity + 20)
    else:
        return Result(velocity=config.base_velocity)


def steer(
        data: Data, difference_data: Difference
) -> Result:
    if data.l[2] < 320 and data.r[2] < 321:
        if data.l[2] / difference_data.l[2] < data.r[2] / difference_data.r[2]:
            return Result(steer=(difference_data.l[2] - data.l[2]) / 3)
        else:
            return Result(steer=(data.r[2] - difference_data.r[2]) / 3)
    elif data.l[2] < 320:
        return Result(steer=(difference_data.l[2] - data.l[2]) / 3 - 10)
    elif data.r[2] < 321:
        return Result(steer=(data.r[2] - difference_data.r[2]) / 3 + 10)


def curve(
        data: Data, difference_data: Difference
) -> Result:
    if data.v[3] < difference_data.base_v:
        if data.v[2] > data.v[3] > data.v[4] or (data.v[2] > data.v[3] and data.v[4] <= 55 and data.v[3] <= 30):
            return Result(
                situation="곡선 좌회전",
                steer=(data.r[2] - difference_data.r[2]) / 2.2 - 10,
                velocity=config.base_velocity
            )
        elif data.v[2] < data.v[3] < data.v[4] or (data.v[4] > data.v[3] and data.v[2] <= 55 and data.v[3] <= 30):
            return Result(
                situation="곡선 우회전",
                steer=(difference_data.l[2] - data.l[2]) / 2.2 + 10,
                velocity=config.base_velocity
            )
        else:
            return Result(situation="곡선 상태 유지", steer=data.last_steer, velocity=config.base_velocity - 15)
    else:
        return Result()


def left_right_angle(
        data: Data
) -> Result:
    situation = "직각 좌회전"
    if data.v[5] <= data.v[4] <= data.v[3] < 170 and -15 < (data.v[6] + data.v[4]) / 2 - data.v[5] < 15:
        return Result(situation=situation, steer=config.left_steer)
    else:
        return Result()


def right_right_angle(
        data: Data
) -> Result:
    situation = "직각 우회전"
    if data.v[1] <= data.v[2] <= data.v[3] < 170 and -15 < (data.v[0] + data.v[2]) / 2 - data.v[1] < 15:
        return Result(situation=situation, steer=config.right_steer)
    else:
        return Result()


def four_lane(
        data: Data, direction: Direction = Direction.Stop
) -> Result:
    situation = "사차선"
    if data.l[1] + data.l[2] == 640 and \
            data.r[1] + data.r[2] == 642 and \
            data.v[3] < 110:
        if direction == Direction.Straight:
            return Result(situation=situation, steer=0)
        elif direction == Direction.Left:
            return Result(situation=situation, steer=config.left_steer)
        elif direction == Direction.Right:
            return Result(situation=situation, steer=config.right_steer)
    else:
        return Result()


def left_three_lane(
        data: Data, direction: Direction = Direction.Stop
) -> Result:
    situation = "ㅓ자 삼차선"
    if -15 < (data.v[4] + data.v[6]) / 2 - data.v[5] < 15 and data.l[1] + data.l[2] == 640 and data.v[3] > 200:
        if direction == Direction.Straight:
            return Result(situation=situation, steer=0)
        elif direction == Direction.Left:
            return Result(situation=situation, steer=config.left_steer)
    else:
        return Result()


def right_three_lane(
        data: Data, direction: Direction = Direction.Stop
) -> Result:
    situation = "ㅏ자 삼차선"
    if -10 < (data.v[2] + data.v[0]) / 2 - data.v[1] < 10 and data.r[1] + data.r[2] == 642 and data.v[3] > 200:
        if direction == Direction.Straight:
            return Result(situation=situation, steer=0)
        elif direction == Direction.Right:
            return Result(situation=situation, steer=config.right_steer)
    else:
        return Result()


def t_three_lane(
        data: Data, direction: Direction = Direction.Stop
) -> Result:
    situation = "T자 삼차선"
    if data.l[1] + data.r[1] == 641 and \
            50 <= data.v[2] < 175 and 50 <= data.v[3] < 175 and 50 <= data.v[4] < 175:
        if direction == Direction.Stop:
            return Result(situation=situation, velocity=0)
        elif direction == Direction.Left:
            return Result(situation=situation, steer=config.left_steer, velocity=config.base_velocity - 5)
        elif direction == Direction.Right:
            return Result(situation=situation, steer=config.right_steer, velocity=config.base_velocity - 5)
        return Result()


def exit_left_dot_line(
        data: Data, difference_data: Difference
) -> Result:
    situation = "좌측 점선 인식 및 탈출"
    if data.v[6] < data.v[5] < data.v[4] < data.v[3] < data.v[2] > data.v[1] > data.v[6] and \
            data.v[3] < difference_data.base_v + 30:
        module.hold_frame = True, 5
        return Result(
            situation=situation,
            steer=config.left_steer
        )
    return Result()


def exit_right_dot_line(
        data: Data, difference_data: Difference
) -> Result:
    situation = "우측 점선 인식 및 탈출"
    if data.v[0] < data.v[1] < data.v[2] < data.v[3] < data.v[4] > data.v[5] > data.v[6] and \
            data.v[3] < difference_data.base_v + 30:
        module.hold_frame = True, 5
        return Result(
            situation=situation,
            steer=config.right_steer
        )
    return Result()


def lidar_scan(
        data: Data, direction: Direction = Direction.Stop, scan_distance: int = 230
) -> Result:
    situation = "장애물 인식"
    if 0 < data.front_lidar < scan_distance:
        module.hold_frame = True, 5
        if direction == Direction.Straight:
            return Result(situation=situation, steer=0, velocity=None)
        elif direction == Direction.Left:
            return Result(situation=situation, steer=config.left_steer - 15, velocity=None)
        elif direction == Direction.Right:
            return Result(situation=situation, steer=config.right_steer + 15, velocity=None)
        else:
            return Result(situation=situation, steer=0, velocity=0)
    else:
        return Result()


# Warning: Experimental Feature
def back_car(
        data: Data, scan_v_distance: int = 60, scan_lidar_distance: int = 160
) -> Result:
    if 0 < data.front_lidar < scan_lidar_distance:
        module.hold_frame = True, 5
        return Result(
            situation="라이다 초근접 인식 후진",
            steer=-non_op.get_last_result().steer / 2,
            velocity=-config.base_velocity / 2
        )
    elif (data.v[2] < scan_v_distance or data.v[2] == 255) and \
            (data.v[3] < scan_v_distance or data.v[3] == 255) and \
            (data.v[4] < scan_v_distance or data.v[4] == 255):
        module.hold_frame = True, 5
        return Result(
            situation="V 초근접 인식 후진",
            steer=-util.not_none(non_op.get_last_result().steer, 0) / 2,
            velocity=-config.base_velocity / 2
        )
    return Result()


def hold_result() -> Result:
    if not module.hold_frame[0] and module.hold_frame[1] > 0:
        module.hold_frame = False, module.hold_frame[1] - 1
        return Result(
            situation="프레임 유지 - " + util.not_none(module.last_result.situation, "").replace("프레임 유지 - ", ""),
            steer=module.last_result.steer,
            velocity=module.last_result.velocity
        )
    elif module.hold_frame[0]:
        module.hold_frame = False, module.hold_frame[1]
    return Result()


def manual_drive() -> Result:
    w = ["W", "w", "8", "up"]
    s = ["S", "s", "2", "down"]
    a = ["A", "a", "4", "left"]
    d = ["D", "d", "5", "right"]
    wa = ["7", "home"]
    wd = ["9", "page up"]
    sa = ["1", "end"]
    sd = ["3", "page down"]
    stop = ["5", "clear"]
    if util.detect_keys(w + s + a + d + wa + wd + sa + sd + stop):
        situation = "수동주행 "
        manual_steer = 0
        manual_velocity = 0
        module.hold_frame = False, 0
        if util.detect_keys(w):
            situation += "↑"
            manual_velocity = config.base_velocity
        elif util.detect_keys(s):
            situation += "↓"
            manual_velocity = -config.base_velocity
        if util.detect_keys(a):
            situation += "←"
            manual_steer += config.left_steer
            manual_velocity = util.change_absolute_value(manual_velocity, -15)
        elif util.detect_keys(d):
            situation += "→"
            manual_steer += config.right_steer
            manual_velocity = util.change_absolute_value(manual_velocity, -15)
        if util.detect_keys(wa):
            situation += "↖"
            manual_steer += config.left_steer
            manual_velocity = config.base_velocity - 15
        elif util.detect_keys(wd):
            situation += "↗"
            manual_steer += config.right_steer
            manual_velocity = config.base_velocity - 15
        elif util.detect_keys(sa):
            situation += "↙"
            manual_steer -= 70
            manual_velocity = -config.base_velocity + 15
        elif util.detect_keys(sd):
            situation += "↘"
            manual_steer += config.right_steer
            manual_velocity = -config.base_velocity + 15
        elif util.detect_keys(stop):
            situation += "▣"
            manual_steer = 0
            manual_velocity = 0
        return Result(situation=situation, steer=manual_steer, velocity=manual_velocity)
    else:
        return Result()


class non_op:
    @staticmethod
    def esc_to_halt():
        if keyboard.is_pressed("esc"):
            sys.stdout.write(
                "\n" +
                "\n" +
                "System ended by pressing ESC"
            )
            # halt.halt()
            sys.exit(0)

    @staticmethod
    def control_current_velocity(
            current_velocity: int
    ) -> int:  # Return New Current Velocity
        shift = ["shift", "*"]
        control = ["control", "/"]
        if util.detect_keys(shift):
            return util.change_absolute_value(current_velocity, 25)
        elif util.detect_keys(control):
            return util.change_absolute_value(current_velocity, -25)
        return current_velocity

    @staticmethod
    def control_base_velocity():
        if util.detect_keys(["+", "="]):
            config.base_velocity += 1
        elif util.detect_keys(["-", "_"]):
            config.base_velocity -= 1

    @staticmethod
    def save_result(result: Result):
        module.last_result = result

    @staticmethod
    def get_last_result():
        return last_result
