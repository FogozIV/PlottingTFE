import dataclasses
import struct
from typing import Optional

from data.Parser import CustomParser


@dataclasses.dataclass
class CurveBenchmark:
    current_error: Optional[float] = None  # 0
    error: Optional[float] = None          # 1
    dt: Optional[float] = None             # 2
    robot_dt: Optional[float] = None       # 3
    translational_position: Optional[float] = None  # 4
    translational_target: Optional[float] = None    # 5
    left_pwm: Optional[float] = None       # 6
    right_pwm: Optional[float] = None      # 7
    x: Optional[float] = None              # 8
    y: Optional[float] = None              # 9
    a: Optional[float] = None              # 10
    target_x: Optional[float] = None       # 11
    target_y: Optional[float] = None       # 12
    up: Optional[float] = None             # 13
    ui: Optional[float] = None             # 14
    ud: Optional[float] = None             # 15
    uff: Optional[float] = None            # 16
    raw_ud: Optional[float] = None         # 17
    up_angle: Optional[float] = None       # 18
    ui_angle: Optional[float] = None       # 19
    ud_angle: Optional[float] = None       # 20
    uff_angle: Optional[float] = None      # 21
    raw_ud_angle: Optional[float] = None   # 22
@dataclasses.dataclass
class CurveBenchmarkV01:
    current_error: Optional[float] = None                # 0
    error: Optional[float] = None                        # 1
    dt: Optional[float] = None                           # 2
    robot_dt: Optional[float] = None                     # 3
    translational_position: Optional[float] = None       # 4
    translational_target: Optional[float] = None         # 5
    rotational_position_deg: Optional[float] = None          # 6
    rotational_target_deg: Optional[float] = None            # 7
    translational_speed_estimation: Optional[float] = None       # 8
    rotational_speed_estimation: Optional[float] = None          # 9
    translational_speed_estimation_2: Optional[float] = None     # 10
    rotational_speed_estimation_2: Optional[float] = None        # 11
    translational_ramp_speed: Optional[float] = None     # 12
    rotational_ramp_speed: Optional[float] = None        # 13
    left_pwm: Optional[float] = None                     # 14
    right_pwm: Optional[float] = None                    # 15
    x: Optional[float] = None                            # 16
    y: Optional[float] = None                            # 17
    a: Optional[float] = None                            # 18
    target_x: Optional[float] = None                     # 19
    target_y: Optional[float] = None                     # 20
    up: Optional[float] = None                           # 21
    ui: Optional[float] = None                           # 22
    ud: Optional[float] = None                           # 23
    uff: Optional[float] = None                          # 24
    raw_ud: Optional[float] = None                       # 25
    up_angle: Optional[float] = None                     # 26
    ui_angle: Optional[float] = None                     # 27
    ud_angle: Optional[float] = None                     # 28
    uff_angle: Optional[float] = None                    # 29
    raw_ud_angle: Optional[float] = None                 # 30

def generateBitMaskFor11(subversion, subsubversion):
    bitmask = 0
    base_indices = list(range(0, 24)) + list(range(26,29))
    for i in base_indices:
        bitmask |= 1 << i
    if subversion in (2, 3):
        bitmask |= 1 << (22 + subversion)  # 2 → 24 3 → 25

    if subsubversion in (2, 3):
        bitmask |= 1 << (27 + subsubversion)  # 2 → 29, 3 → 30
    return bitmask

def generateBitMaskFor10(subversion, subsubversion):
    bitmask = 0
    base_indices = list(range(0, 16)) + [18, 19, 20]
    for i in base_indices:
        bitmask |= 1 << i

    if subversion in (2, 3):
        bitmask |= 1 << (14 + subversion)  # 2 → 16 3 → 17

    if subsubversion in (2, 3):
        bitmask |= 1 << (19 + subsubversion)  # 2 → 21, 3 → 22
    return bitmask
class CurveBenchmarkParser(CustomParser[CurveBenchmark]):
    dataclass_type = CurveBenchmark
    bitmask_function = generateBitMaskFor10

class CurveBenchmarkParserV01(CustomParser[CurveBenchmarkV01]):
    dataclass_type = CurveBenchmarkV01
    bitmask_function = generateBitMaskFor11