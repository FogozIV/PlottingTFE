import dataclasses
import struct
from itertools import accumulate

from data.CompleteParserClasses import *
from data.CurveBenchmarkClasses import *
from data.ZieglerNicholsClasses import ZieglerNicholsParser


@dataclasses.dataclass
class AngleData:
    current_error: float
    error: float
    dt: float
    robot_dt: float
    rotational_target_deg: float
    rotational_position_deg: float
    @staticmethod
    def get_length():
        return 48

    @staticmethod
    def from_bytes(data: bytes) -> 'AngleData':
        if len(data) < AngleData.get_length():
            raise ValueError(f'Not enough bytes to unpack AngleData (need ${AngleData.get_length()} bytes)')
        values = struct.unpack('>6d', data)  # > = big-endian, 6 doubles
        return AngleData(*values)
@dataclasses.dataclass
class DistanceData:
    current_error: float
    error: float
    dt: float
    robot_dt: float
    translational_position: float
    translational_target: float

    @staticmethod
    def get_length():
        return 48

    @staticmethod
    def from_bytes(data: bytes) -> 'DistanceData':
        if len(data) < DistanceData.get_length():
            raise ValueError(f'Not enough bytes to unpack DistanceData (need {DistanceData.get_length()} bytes)')
        values = struct.unpack('>6d', data)  # > = big-endian, 6 doubles
        return DistanceData(*values)

@dataclasses.dataclass
class DistanceDataSuperBase:
    current_error: float
    error: float
    dt: float
    robot_dt: float
    translational_position: float
    translational_target: float
    left_pwm: float
    right_pwm: float
    @staticmethod
    def get_length():
        return 8*8

    @staticmethod
    def from_bytes(data: bytes) -> 'DistanceDataSuperBase':
        if len(data) < DistanceDataSuperBase.get_length():
            raise ValueError(f'Not enough bytes to unpack DistanceData (need {DistanceDataSuperBase.get_length()} bytes)')
        values = struct.unpack('>8d', data)  # > = big-endian, 6 doubles
        return DistanceDataSuperBase(*values)

@dataclasses.dataclass
class DistanceDataBase(DistanceDataSuperBase):
    up: float
    ui: float
    ud: float

@dataclasses.dataclass
class DistanceDataPID(DistanceDataBase):
    @staticmethod
    def get_length():
        return 88  # 11 doubles × 8 bytes each

    @staticmethod
    def from_bytes(data: bytes) -> 'DistanceDataPID':
        if len(data) < DistanceDataPID.get_length():
            raise ValueError(f'Not enough bytes to unpack DistanceDataPID (need {DistanceDataPID.get_length()} bytes)')
        values = struct.unpack('>11d', data)
        return DistanceDataPID(*values)


@dataclasses.dataclass
class DistanceDataPIDSpeedFF(DistanceDataBase):
    uff: float

    @staticmethod
    def get_length():
        return 96  # 12 doubles × 8 bytes each

    @staticmethod
    def from_bytes(data: bytes) -> 'DistanceDataPIDSpeedFF':
        if len(data) < DistanceDataPIDSpeedFF.get_length():
            raise ValueError(f'Not enough bytes to unpack DistanceDataPIDSpeedFF (need {DistanceDataPIDSpeedFF.get_length()} bytes)')
        values = struct.unpack('>12d', data)
        return DistanceDataPIDSpeedFF(*values)
@dataclasses.dataclass
class DistanceAngleData:
    summed_error: float
    error: float
    dt: float
    robot_dt: float
    current_error_angle: float
    current_error_distance: float
    translational_position: float
    translational_target: float
    rotational_position_deg: float
    rotational_target_deg: float
    current_x: float
    current_y: float

    @staticmethod
    def get_length():
        return 96  # 12 doubles * 8 bytes each

    @staticmethod
    def from_bytes(data: bytes) -> 'DistanceAngleData':
        if len(data) < DistanceAngleData.get_length():
            raise ValueError(f'Not enough bytes to unpack DistanceAngleData (need {DistanceAngleData.get_length()} bytes)')
        values = struct.unpack('>12d', data)
        return DistanceAngleData(*values)

@dataclasses.dataclass
class AngleSpeedComparisonData:
    current_error: float
    error: float
    dt: float
    robot_dt: float
    rotational_target_deg: float
    rotational_position_deg: float
    ramp_speed_deg: float
    estimated_speed_deg: float
    other_estimated_speed_deg: float

    @staticmethod
    def get_length():
        return 72  # 9 doubles

    @staticmethod
    def from_bytes(data: bytes) -> 'AngleSpeedComparisonData':
        if len(data) < AngleSpeedComparisonData.get_length():
            raise ValueError(f'Not enough bytes to unpack AngleSpeedComparisonData (need {AngleSpeedComparisonData.get_length()} bytes)')
        values = struct.unpack('>9d', data)
        return AngleSpeedComparisonData(*values)
@dataclasses.dataclass
class AnglePWMData:
    current_error: float
    error: float
    dt: float
    robot_dt: float
    rotational_target_deg: float
    rotational_position_deg: float
    left_pwm: float
    right_pwm: float

    @staticmethod
    def get_length():
        return 64  # 8 * 8 bytes

    @staticmethod
    def from_bytes(data: bytes) -> 'AnglePWMData':
        if len(data) < AnglePWMData.get_length():
            raise ValueError(f'Not enough bytes to unpack AnglePWMData (need {AnglePWMData.get_length()} bytes)')
        values = struct.unpack('>8d', data)
        return AnglePWMData(*values)

@dataclasses.dataclass
class DistancePWMData:
    current_error: float
    error: float
    dt: float
    robot_dt: float
    translational_position: float
    translational_target: float
    left_pwm: float
    right_pwm: float

    @staticmethod
    def get_length():
        return 64

    @staticmethod
    def from_bytes(data: bytes) -> 'DistancePWMData':
        if len(data) < DistancePWMData.get_length():
            raise ValueError(f'Not enough bytes to unpack DistancePWMData (need {DistancePWMData.get_length()} bytes)')
        values = struct.unpack('>8d', data)
        return DistancePWMData(*values)
@dataclasses.dataclass
class AngleSpeedData:
    rotational_position_deg: float
    rotational_target_deg: float
    ramp_speed_deg: float
    estimated_speed_deg: float
    robot_dt: float
    left_pwm: float
    right_pwm: float
    dt: float = 0.0
    needs_dt_accumulation = True  # mark this class as needing accumulation

    @staticmethod
    def get_length():
        return 56  # 7 * 8 bytes

    @staticmethod
    def from_bytes(data: bytes) -> 'AngleSpeedData':
        if len(data) < AngleSpeedData.get_length():
            raise ValueError(f'Not enough bytes to unpack AngleSpeedData (need {AngleSpeedData.get_length()} bytes)')
        values = struct.unpack('>7d', data)
        return AngleSpeedData(*values)

@dataclasses.dataclass
class DistanceSpeedData:
    translational_position: float
    translational_target: float
    ramp_speed: float
    estimated_speed: float
    robot_dt: float
    left_pwm: float
    right_pwm: float
    dt: float = 0.0
    needs_dt_accumulation = True  # mark this class as needing accumulation

    @staticmethod
    def get_length():
        return 56

    @staticmethod
    def from_bytes(data: bytes) -> 'DistanceSpeedData':
        if len(data) < DistanceSpeedData.get_length():
            raise ValueError(f'Not enough bytes to unpack DistanceSpeedData (need {DistanceSpeedData.get_length()} bytes)')
        values = struct.unpack('>7d', data)
        return DistanceSpeedData(*values)

versions = [
    AngleData,                   # 0: BENCHMARK_LEGACY_ANGLE
    DistanceData,                # 1: BENCHMARK_LEGACY_DISTANCE
    DistanceAngleData,           # 2: BENCHMARK_LEGACY_DISTANCE_ANGLE
    AngleSpeedComparisonData,    # 3: BENCHMARK_ANGLE_V_0_1
    [None, DistanceDataPID, DistanceDataPIDSpeedFF, DistanceDataSuperBase], # 4: BENCHMARK_DISTANCE_V_0_1
    BenchmarkDistanceAngleV01,           # 5: BENCHMARK_DISTANCE_ANGLE_V_0_1
    ZieglerNicholsParser,                # 6: Z_N_LEGACY_ANGLE
    DistancePWMData,             # 7: Z_N_LEGACY_DISTANCE
    AngleSpeedData,              # 8: Z_N_LEGACY_ANGLE_SPEED
    DistanceSpeedData,           # 9: Z_N_LEGACY_DISTANCE_SPEED
    CurveBenchmarkParser,        # 10 : BENCHMARK_LEGACY_CURVE
    CurveBenchmarkParserV01,      # 11 : BENCHMARK_CURVE_V_0_1
    BenchmarkAngleV02,
    BenchmarkDistanceV02,
    UniversalBenchmarkV01

]