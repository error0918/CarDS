from typing import List
import sys
import keyboard

"""
CarDS - internal.util.py
Copyright 2023. jtaeyeon05 all rights reserved 
"""


def run_message(name: str):
    sys.stdout.write(
        "CarDS - " + name + "\n" +
        "Copyright 2023. jtaeyeon05 all rights reserved " +
        "\n" +
        "\n" +
        "\n"
    )


def detect_keys(keys: List[str]) -> bool:
    return True in map(keyboard.is_pressed, keys)


def change_absolute_value(value: int, delta: int) -> int:
    if value < 0:
        return value - delta
    elif value > 0:
        return value + delta
    else:
        return 0


def not_none(value, if_none):
    return if_none if value is None else value
