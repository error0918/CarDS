from typing import List
import keyboard

"""
CarDS - internal.util.py
Copyright 2023. jtaeyeon05 all rights reserved 
"""


def detect_keys(keys: List[str]) -> bool:
    return list(map(keyboard.is_pressed, keys)).index(True) != -1


def change_absolute_value(value: int, delta: int) -> int:
    if value < 0:
        return value - delta
    elif value > 0:
        return value + delta
    else:
        return 0