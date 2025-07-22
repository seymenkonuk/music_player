# ============================================================================
# File:    timeUtils.py
# Author:  Recep Seymen Konuk <konukrecepseymen@gmail.com>
#
# Licensed under the terms of the LICENSE file in the project root directory.
# ============================================================================

def seconds_to_time(second: int):
    result = ""

    hours = (second // 3600) % 100
    if hours < 10:
        result += "0"
    result += str(hours)

    result += ":"

    minutes = (second // 60) % 60
    if minutes < 10:
        result += "0"
    result += str(minutes)

    result += ":"

    seconds = (second // 1) % 60
    if seconds < 10:
        result += "0"
    result += str(seconds)

    return result
