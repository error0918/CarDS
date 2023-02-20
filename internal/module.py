from enum import Enum
from config import data_type
from config import result_type
from internal import halt
from internal import util
from typing import List
import config
import keyboard

"""
CarDS - internal.module.py
Copyright 2023. jtaeyeon05 all rights reserved
"""


class Direction(Enum):
    Straight = 1
    Left = 2
    Right = 3
    Stop = 4


def operation(
        result_list: List[result_type]
) -> result_type:
    result: result_type = (None, None, None)
    for op_result in result_list:
        if op_result is not None:
            op_list = list(op_result)
            result = util.not_none(op_list[0], result[0]), \
                util.not_none(op_list[1], result[1]), \
                util.not_none(op_list[2], result[2])
    return result


def default(
        data: data_type, difference_data
) -> result_type:
    return operation(
        result_list=[
            velocity(data=data),
            steer(data=data, difference_data=difference_data),
            curve(data=data, difference_data=difference_data),
            left_right_angle(data=data),
            right_right_angle(data=data)
        ]
    )


def velocity(
        data: data_type
) -> result_type:
    if data[2][0] < data[2][1] < data[2][2] < data[2][3] \
            and data[2][3] > data[2][4] > data[2][5] > data[2][6] \
            and -10 < 2 * data[2][5] - (data[2][4] + data[2][6]) < 10 \
            and -10 < 2 * data[2][1] - (data[2][0] + data[2][2]) < 10:
        return "직진", None, config.base_velocity + 20
    else:
        return None, None, config.base_velocity


def steer(
        data: data_type, difference_data
) -> result_type:
    if data[3][2] < 320 and data[4][2] < 321:
        if data[3][2] / difference_data["l"][2] < data[4][2] / difference_data["r"][2]:
            return None, (difference_data["l"][2] - data[3][2]) / 3 + 20, None
        else:
            return None, (data[4][2] - difference_data["r"][2]) / 3 + 20, None
    elif data[3][2] < 320:
        return None, (difference_data["l"][2] - data[3][2]) / 3 - 10, None
    elif data[4][2] < 321:
        return None, (data[4][2] - difference_data["r"][2]) / 3 + 10, None


def curve(
        data: data_type, difference_data
) -> result_type:
    if data[2][3] < 120:
        if data[2][2] > data[2][3] > data[2][4]:
            return "곡선 좌회전", (data[4][2] - difference_data["r"][2]) / 3 - 10, config.base_velocity - 15
        elif data[2][2] < data[2][3] < data[2][4]:
            return "곡선 우회전", (difference_data["l"][2] - data[3][2]) / 3 + 10, config.base_velocity - 15
        else:
            return "곡선 상태 유지", data[1], config.base_velocity - 15
    else:
        return None, None, None


def left_right_angle(
        data: data_type
) -> result_type:
    if -15 < (data[2][6] + data[2][3]) - (data[2][4] + data[2][5]) < 15 \
            and data[2][5] < 160 and data[2][0] > 64 and data[2][2] < data[2][6]:
        situation = "직각 자회전"
        return situation, config.right_steer, None
    else:
        return None, None, None


def right_right_angle(
        data: data_type
) -> result_type:
    if -15 < (data[2][6] + data[2][3]) - (data[2][4] + data[2][5]) < 15 \
            and data[2][5] < 160 and data[2][0] > 64 and data[2][2] < data[2][6]:
        situation = "직각 우회전"
        return situation, config.right_steer, None
    else:
        return None, None, None


def four_lane(
        data: data_type, direction: Direction = Direction.Stop
) -> result_type:
    if data[3][1] + data[3][2] == 640 and \
            data[4][1] + data[4][2] == 642 and \
            data[2][3] < 120:
        situation = "사차선"
        if direction == Direction.Straight:
            return situation, 0, None
        elif direction == Direction.Left:
            return situation, config.left_steer, None
        elif direction == Direction.Right:
            return situation, config.right_steer, None
    else:
        return None, None, None


def left_three_lane(
        data: data_type, direction: Direction = Direction.Stop
) -> result_type:
    if data[3][1] + data[3][2] == 640 and data[4][1] + data[4][2] == 642 and data[2][3] < 120:
        situation = "ㅓ자 삼차선"
        if direction == Direction.Straight:
            return situation, 0, None
        elif direction == Direction.Left:
            return situation, config.left_steer, None
    else:
        return None, None, None


def right_three_lane(
        data: data_type, direction: Direction = Direction.Stop
) -> result_type:
    if data[3][1] + data[3][2] == 640 and data[4][1] + data[4][2] == 642 and data[2][3] < 120:
        situation = "ㅏ자 삼차선"
        if direction == Direction.Straight:
            return situation, 0, None
        elif direction == Direction.Right:
            return situation, config.right_steer, None
    else:
        return None, None, None


# TODO
def t_three_lane(
        data: data_type, direction: Direction = Direction.Stop
) -> result_type:
    return None, None, None


def lidar_scan(
        data: data_type, direction: Direction = Direction.Stop, scan_distance: int = 400
) -> result_type:
    situation = "장애물 인식"
    if 0 < data[0] < scan_distance:
        if direction == Direction.Straight:
            return situation, 0, None
        elif direction == Direction.Left:
            return situation, config.left_steer, None
        elif direction == Direction.Right:
            return situation, config.right_steer, None
        else:
            return situation, 0, 0
    else:
        return None, None, None


# TODO: Use on Real Situation
def manual_drive() -> result_type:
    w = ["W", "w", "8", "up"]
    s = ["S", "s", "2", "down"]
    a = ["A", "a", "4", "left"]
    d = ["D", "d", "5", "right"]
    wa = ["7", "home"]
    wd = ["9", "page up"]
    sa = ["1", "end"]
    sd = ["3", "page down"]
    shift = ["shift", "*"]
    control = ["control", "/"]
    stop = ["5", "clear"]
    if util.detect_keys(w + s + a + d + wa + wd + sa + sd + shift + control + stop):
        situation = "수동주행 "
        manual_steer = 0
        manual_velocity = 0
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
        if util.detect_keys(shift):
            situation += "⇈"
            manual_velocity = util.change_absolute_value(manual_velocity, 25)
        elif util.detect_keys(control):
            situation += "⇊"
            manual_velocity = util.change_absolute_value(manual_velocity, -25)
        elif util.detect_keys(stop):
            situation += "▣"
            manual_steer = 0
            manual_velocity = 0
        return situation, manual_steer, manual_velocity
    else:
        return None, None, None


# TODO: Use on Real Situation
def esc_to_halt():
    if keyboard.is_pressed("esc"):
        halt.halt()


# TODO: Use on Real Situation
def control_base_velocity():
    if util.detect_keys(["+", "="]):
        config.base_velocity += 1
    elif util.detect_keys(["-", "_"]):
        config.base_velocity -= 1
