from enum import Enum
from data.data import *
from data.result import *
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
        data: Data, difference_data
) -> Result:
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
        data: Data
) -> Result:
    if data.v[0] < data.v[1] < data.v[2] < data.v[3] \
            and data.v[3] > data.v[4] > data.v[5] > data.v[6] \
            and -10 < 2 * data.v[5] - (data.v[4] + data.v[6]) < 10 \
            and -10 < 2 * data.v[1] - (data.v[0] + data.v[2]) < 10:
        return Result(situation="직진", velocity=config.base_velocity + 20)
    else:
        return Result(velocity=config.base_velocity)


def steer(
        data: Data, difference_data
) -> Result:
    if data.l[2] < 320 and data.r[2] < 321:
        if data.l[2] / difference_data["l"][2] < data.r[2] / difference_data["r"][2]:
            return Result(steer=(difference_data["l"][2] - data.l[2]) / 3 + 20)
        else:
            return Result(steer=(data.r[2] - difference_data["r"][2]) / 3 + 20)
    elif data.l[2] < 320:
        return Result(steer=(difference_data["l"][2] - data.l[2]) / 3 - 10)
    elif data.r[2] < 321:
        return Result(steer=(data.r[2] - difference_data["r"][2]) / 3 + 10)


def curve(
        data: Data, difference_data
) -> Result:
    if data.v[3] < 120:
        if data.v[2] > data.v[3] > data.v[4]:
            return Result(
                situation="곡선 좌회전",
                steer=(data.r[2] - difference_data["r"][2]) / 3 - 10,
                velocity=config.base_velocity - 15
            )
        elif data.v[2] < data.v[3] < data.v[4]:
            return Result(
                situation="곡선 우회전",
                steer=(difference_data["l"][2] - data.l[2]) / 3 + 10,
                velocity=config.base_velocity - 15
            )
        else:
            return Result(situation="곡선 상태 유지", steer=data.last_steer, velocity=config.base_velocity - 15)
    else:
        return Result()


def left_right_angle(
        data: Data
) -> Result:
    if -15 < (data.v[6] + data.v[3]) - (data.v[4] + data.v[5]) < 15 \
            and data.v[5] < 160 and data.v[0] > 64 and data.v[2] < data.v[6]:
        situation = "직각 자회전"
        return Result(situation=situation, steer=config.right_steer)
    else:
        return Result()


def right_right_angle(
        data: Data
) -> Result:
    if -15 < (data.v[6] + data.v[3]) - (data.v[4] + data.v[5]) < 15 \
            and data.v[5] < 160 and data.v[0] > 64 and data.v[2] < data.v[6]:
        situation = "직각 우회전"
        return Result(situation=situation, steer=config.right_steer)
    else:
        return Result()


def four_lane(
        data: Data, direction: Direction = Direction.Stop
) -> Result:
    if data.l[1] + data.l[2] == 640 and \
            data.r[1] + data.r[2] == 642 and \
            data.v[3] < 120:
        situation = "사차선"
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
    if data.l[1] + data.l[2] == 640 and data.r[1] + data.r[2] == 642 and data.v[3] < 120:
        situation = "ㅓ자 삼차선"
        if direction == Direction.Straight:
            return Result(situation=situation, steer=0)
        elif direction == Direction.Left:
            return Result(situation=situation, steer=config.left_steer)
    else:
        return Result()


def right_three_lane(
        data: Data, direction: Direction = Direction.Stop
) -> Result:
    if data.l[1] + data.l[2] == 640 and data.r[1] + data.r[2] == 642 and data.v[3] < 120:
        situation = "ㅏ자 삼차선"
        if direction == Direction.Straight:
            return Result(situation=situation, steer=0)
        elif direction == Direction.Right:
            return Result(situation=situation, steer=config.right_steer)
    else:
        return Result()


# TODO
def t_three_lane(
        data: Data, direction: Direction = Direction.Stop
) -> Result:
    return Result(situation=None, steer=None, velocity=None)


def lidar_scan(
        data: Data, direction: Direction = Direction.Stop, scan_distance: int = 400
) -> Result:
    situation = "장애물 인식"
    if 0 < data.front_lidar < scan_distance:
        if direction == Direction.Straight:
            return Result(situation=situation, steer=0, velocity=None)
        elif direction == Direction.Left:
            return Result(situation=situation, steer=config.left_steer, velocity=None)
        elif direction == Direction.Right:
            return Result(situation=situation, steer=config.right_steer, velocity=None)
        else:
            return Result(situation=situation, steer=0, velocity=0)
    else:
        return Result()


# TODO: Use on Real Situation
def manual_drive() -> Result:
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
        return Result(situation=situation, steer=manual_steer, velocity=manual_velocity)
    else:
        return Result()


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
