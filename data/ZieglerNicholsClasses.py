import dataclasses
import struct
from typing import Optional

from data.Parser import CustomParser


@dataclasses.dataclass
class ZieglerNichols:
    position: Optional[float] = None  # 0
    target: Optional[float] = None    # 1
    ramp_speed: Optional[float] = None  # 2
    estimated_speed: Optional[float] = None  # 3
    robot_dt: Optional[float] = None        # 4
    left_pwm: Optional[float] = None  # 5
    right_pwm: Optional[float] = None # 6
    dt: Optional[float] = 0.0

class ZieglerNicholsParser(CustomParser[ZieglerNichols]):
    dataclass_type = ZieglerNichols
    bitmask_function = lambda x,y: 2**7 -1

