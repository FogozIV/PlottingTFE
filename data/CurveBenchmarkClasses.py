import dataclasses
import struct

@dataclasses.dataclass
class CurveBenchmarkBase:
    current_error: float
    error: float
    dt: float
    robot_dt: float
    translational_position: float
    translational_target: float
    left_pwm: float
    right_pwm: float
    x: float
    y: float
    a: float
    target_x: float
    target_y: float
    up: float
    ui: float
    ud: float
    up_angle: float
    ui_angle: float
    ud_angle: float

@dataclasses.dataclass
class BenchmarkPIDPID(CurveBenchmarkBase):

    @staticmethod
    def get_length():
        return 8 * 19  # 14 doubles

    @staticmethod
    def from_bytes(data: bytes) -> 'BenchmarkPIDPID':
        if len(data) < BenchmarkPIDPID.get_length():
            raise ValueError("Not enough data")
        values = struct.unpack('>19d', data)
        return BenchmarkPIDPID(*values)

@dataclasses.dataclass
class BenchmarkPIDFFPID(CurveBenchmarkBase):
    uff: float

    @staticmethod
    def get_length():
        return 8 * 20

    @staticmethod
    def from_bytes(data: bytes) -> 'BenchmarkPIDFFPID':
        if len(data) < BenchmarkPIDFFPID.get_length():
            raise ValueError("Not enough data")
        values = struct.unpack('>20d', data)
        return BenchmarkPIDFFPID(*values)

@dataclasses.dataclass
class BenchmarkPIDPIDFF(CurveBenchmarkBase):
    uff_angle: float

    @staticmethod
    def get_length():
        return 8 * 20

    @staticmethod
    def from_bytes(data: bytes) -> 'BenchmarkPIDPIDFF':
        if len(data) < BenchmarkPIDPIDFF.get_length():
            raise ValueError("Not enough data")
        values = struct.unpack('>20d', data)
        return BenchmarkPIDPIDFF(*values)

@dataclasses.dataclass
class BenchmarkPIDFFPIDFF(CurveBenchmarkBase):
    uff: float
    uff_angle: float

    @staticmethod
    def get_length():
        return 8 * 21

    @staticmethod
    def from_bytes(data: bytes) -> 'BenchmarkPIDFFPIDFF':
        if len(data) < BenchmarkPIDFFPIDFF.get_length():
            raise ValueError("Not enough data")
        values = struct.unpack('>21d', data)
        return BenchmarkPIDFFPIDFF(*values)