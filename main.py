import dataclasses
import struct
from itertools import accumulate
import matplotlib
from math import sqrt
matplotlib.use('QtAgg')

import matplotlib.pyplot as plt
import numpy as np
plt.ion()
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

    @staticmethod
    def get_length():
        return 80

    @staticmethod
    def from_bytes(data: bytes) -> 'DistanceAngleData':
        if len(data) < DistanceAngleData.get_length():
            raise ValueError(f'Not enough bytes to unpack DistanceAngleData (need {DistanceAngleData.get_length()} bytes)')
        values = struct.unpack('>10d', data)  # > = big-endian, 10 doubles
        return DistanceAngleData(*values)


versions = [AngleData, DistanceData, DistanceAngleData]

result = []
with open("BenchmarkController.txt", "rb") as f:
    data = f.read(8)
    if(len(data) != 8):
        raise ValueError("Version of Benchmark not found")
    version = struct.unpack('>Q', data)[0]
    class_type = versions[version]
    while data := f.read(class_type.get_length()):
        result.append(class_type.from_bytes(data))
        print(result[-1])


def plot_translational_tracking(data):
    if not data:
        print("No data to plot.")
        return

    # Use d.dt (accumulated time) as x-axis
    time = [d.dt for d in data]

    # Extract translational values
    target = [d.translational_target for d in data]
    position = [d.translational_position for d in data]

    # Plot
    plt.figure()
    plt.plot(time, target, label="Translational Target")
    plt.plot(time, position, label="Translational Position")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance")
    plt.title("Translational Tracking")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_rotational_tracking(data):
    if not data:
        print("No data to plot.")
        return

    # Use d.dt (accumulated time) as x-axis
    time = [d.dt for d in data]

    # Extract rotational target and position
    target = [d.rotational_target_deg for d in data]
    position = [d.rotational_position_deg for d in data]

    plt.figure()
    plt.plot(time, target, label="Rotational Target (deg)")
    plt.plot(time, position, label="Rotational Position (deg)")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (degrees)")
    plt.title("Rotational Tracking")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)

def plot_error(data):
    if not data:
        print("No data to plot.")
        return
    time = [d.dt for d in data]
    error = [(d.translational_target - d.translational_position) for d in data]
    plt.figure()
    plt.plot(time, error, label="Position error (mm)")
    plt.xlabel("Time (s)")
    plt.ylabel("Position error (mm)")
    plt.title("Translational Tracking")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)

def plot_error_speed(data):
    if not data:
        print("No data to plot.")
        return
    time = [data[i].dt for i in range(len(data)-1)]
    speed = [(data[i+1].translational_position - data[i].translational_position)/data[i].robot_dt for i in range(len(data)-1)]
    plt.figure()
    plt.plot(time, speed, label="Speed of translational (mm/s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (mm/s)")
    plt.title("Translational Tracking")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)

def do_fft(data):
    if not data:
        print("No data to plot.")
        return
    error_signal = np.array([
        d.translational_target - d.translational_position for d in data
    ])

    # Compute sample rate from average robot_dt (in Hz)
    dt_samples = np.array([d.robot_dt for d in data])
    avg_dt = np.mean(dt_samples)
    fs = 1.0 / avg_dt  # sample frequency in Hz
    n = len(error_signal)
    freqs = np.fft.rfftfreq(n, d=avg_dt)  # frequency axis
    spectrum = np.fft.rfft(error_signal)

    # Convert to magnitude spectrum
    magnitude = np.abs(spectrum)

    # Plot
    plt.figure()
    plt.plot(freqs, magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("FFT of Translational Tracking Error")
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)


plot_translational_tracking(result)
plot_error(result)
plot_error_speed(result)
do_fft(result)