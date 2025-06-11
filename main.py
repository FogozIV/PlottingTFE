from data.VersionAndClasses import *
from itertools import accumulate
import matplotlib
from math import sqrt
matplotlib.use('QtAgg')

import matplotlib.pyplot as plt
import numpy as np
plt.ion()

version = None
result = []
class_type = None
with open("BenchmarkController1749419732ANGLE.bin", "rb") as f:
    data = f.read(8)
    if(len(data) != 8):
        raise ValueError("Version of Benchmark not found")
    version = struct.unpack('>Q', data)[0]
    class_type = versions[version]
    while data := f.read(class_type.get_length()):
        result.append(class_type.from_bytes(data))
        print(result[-1])
if all(getattr(d, 'dt', 0.0) == 0.0 for d in result):
    dts = list(accumulate(d.robot_dt for d in result))
    for obj, dt in zip(result, dts):
        obj.dt = dt

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
def plot_rotational_speed_comparison(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    ramp_speed = [d.ramp_speed_deg for d in data]
    estimated_speed = [d.estimated_speed_deg for d in data]
    other_estimated_speed = [d.other_estimated_speed_deg for d in data]

    plt.figure()
    plt.plot(time, ramp_speed, label="Ramp Speed (deg/s)")
    plt.plot(time, estimated_speed, label="Estimated Speed (deg/s)")
    plt.plot(time, other_estimated_speed, label="Other Estimated Speed (deg/s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (deg/s)")
    plt.title("Comparison of Rotational Speeds")
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
def plot_error_speed_vs_pll(data):
    if not data:
        print("No data to plot.")
        return
    time = [data[i].dt for i in range(len(data)-1)]
    time2 = [d.dt for d in data]
    speed = [(data[i+1].rotational_position_deg - data[i].rotational_position_deg)/data[i].robot_dt for i in range(len(data)-1)]
    ramp_speed = [d.ramp_speed_deg for d in data]
    estimated_speed = [d.estimated_speed_deg for d in data]
    plt.figure()
    plt.plot(time2, ramp_speed, label="Ramp Speed (deg/s)")
    plt.plot(time2, estimated_speed, label="Estimated Speed (deg/s)")
    plt.plot(time, speed, label="Speed of Rotational (deg/s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (deg/s)")
    plt.title("Rotational Tracking")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)

def do_fft(data, fct):
    if not data:
        print("No data to plot.")
        return
    error_signal = np.array([
        fct(d) for d in data
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
    return freqs, spectrum, magnitude
def plot_trajectory(data):
    if not data:
        print("No data to plot.")
        return

    x = [d.current_x for d in data]
    y = [d.current_y for d in data]

    plt.figure()
    plt.plot(x, y, marker='o')
    plt.xlabel("X Position (mm)")
    plt.ylabel("Y Position (mm)")
    plt.title("2D Trajectory Tracking")
    plt.grid(True)
    plt.axis('equal')
    plt.tight_layout()
    plt.show(block=True)
def plot_combined_errors(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    angle_errors = [d.current_error_angle for d in data]
    dist_errors = [d.current_error_distance for d in data]

    plt.figure()
    plt.plot(time, dist_errors, label="Distance Error (mm)")
    plt.plot(time, angle_errors, label="Angle Error (deg)")
    plt.xlabel("Time (s)")
    plt.ylabel("Error")
    plt.title("Distance & Angle Error Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_heading_vs_target_heading(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    target = [d.rotational_target_deg for d in data]
    actual = [d.rotational_position_deg for d in data]

    plt.figure()
    plt.plot(time, target, label="Target Heading (deg)")
    plt.plot(time, actual, label="Actual Heading (deg)")
    plt.xlabel("Time (s)")
    plt.ylabel("Heading (deg)")
    plt.title("Heading vs Target Heading")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_heading_error(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    error = [d.rotational_target_deg - d.rotational_position_deg for d in data]  # already in degrees

    plt.figure()
    plt.plot(time, error, label="Heading Error (deg)")
    plt.xlabel("Time (s)")
    plt.ylabel("Error (deg)")
    plt.title("Heading Error Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_rotational_speed(data):
    if len(data) < 2:
        print("Not enough data to compute speed.")
        return

    time = [data[i].dt for i in range(len(data) - 1)]
    speed = [
        (data[i+1].rotational_position_deg - data[i].rotational_position_deg) / data[i].robot_dt
        for i in range(len(data) - 1)
    ]

    plt.figure()
    plt.plot(time, speed, label="Rotational Speed (deg/s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (deg/s)")
    plt.title("Rotational Speed Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_acceleration(data):
    if len(data) < 3:
        print("Not enough data to compute acceleration.")
        return

    time = [data[i].dt for i in range(1, len(data)-1)]
    acceleration = [
        (data[i+1].translational_position - 2 * data[i].translational_position + data[i-1].translational_position)
        / (data[i].robot_dt ** 2)
        for i in range(1, len(data)-1)
    ]

    plt.figure()
    plt.plot(time, acceleration, label="Translational Acceleration (mm/s²)")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (mm/s²)")
    plt.title("Translational Acceleration Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_rotational_tracking_with_pwm(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    target = [d.rotational_target_deg for d in data]
    position = [d.rotational_position_deg for d in data]
    left_pwm = [d.left_pwm for d in data]
    right_pwm = [d.right_pwm for d in data]

    plt.figure()
    plt.plot(time, target, label="Target (deg)")
    plt.plot(time, position, label="Position (deg)")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.title("Rotational Tracking with PWM")
    plt.legend()
    plt.grid(True)

    plt.twinx()
    plt.plot(time, left_pwm, '--', label="Left PWM", alpha=0.6)
    plt.plot(time, right_pwm, '--', label="Right PWM", alpha=0.6)
    plt.ylabel("PWM")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show(block=True)
def plot_translational_tracking_with_pwm(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    target = [d.translational_target for d in data]
    position = [d.translational_position for d in data]
    left_pwm = [d.left_pwm for d in data]
    right_pwm = [d.right_pwm for d in data]

    plt.figure()
    plt.plot(time, target, label="Target")
    plt.plot(time, position, label="Position")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance")
    plt.title("Translational Tracking with PWM")
    plt.legend()
    plt.grid(True)

    plt.twinx()
    plt.plot(time, left_pwm, '--', label="Left PWM", alpha=0.6)
    plt.plot(time, right_pwm, '--', label="Right PWM", alpha=0.6)
    plt.ylabel("PWM")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show(block=True)
def plot_pwm(data):
    if not data:
        print("No data to plot.")
        return
    plt.figure()
    time = [d.dt for d in result]
    plt.plot(time, [d.left_pwm for d in result], label="Left PWM")
    plt.plot(time, [d.right_pwm for d in result], label="Right PWM")
    plt.xlabel("Time (s)")
    plt.ylabel("PWM Value")
    plt.title("Motor PWM Outputs (Angle)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_ramp_vs_estimated_speed(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    ramp_speed = [d.ramp_speed_deg for d in data]
    estimated_speed = [d.estimated_speed_deg for d in data]

    plt.figure()
    plt.plot(time, ramp_speed, label="Ramp Speed (deg/s)")
    plt.plot(time, estimated_speed, label="Estimated Speed (deg/s)")
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (deg/s)")
    plt.title("Ramp Speed vs Estimated Speed")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)

def plot_speed_error(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    error = [d.ramp_speed_deg - d.estimated_speed_deg for d in data]

    plt.figure()
    plt.plot(time, error, label="Speed Error (Ramp - Estimated)")
    plt.xlabel("Time (s)")
    plt.ylabel("Error (deg/s)")
    plt.title("Ramp vs Estimated Speed Error Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)


if version == 0:
    plot_rotational_tracking(result)
    plot_heading_error(result)
    plot_rotational_speed(result)
    do_fft(result, lambda d: (d.rotational_target_deg - d.rotational_position_deg))

elif version == 1:
    plot_translational_tracking(result)
    plot_error(result)
    plot_error_speed(result)
    plot_acceleration(result)

elif version == 2:
    plot_translational_tracking(result)
    plot_rotational_tracking(result)
    plot_trajectory(result)
    plot_combined_errors(result)
    plot_heading_vs_target_heading(result)
    plot_error(result)
    plot_error_speed(result)
elif version == 3:
    plot_rotational_tracking(result)
    plot_heading_error(result)
    plot_rotational_speed_comparison(result)
    plot_rotational_speed(result)
    plot_error_speed_vs_pll(result)
    do_fft(result, lambda d: (d.rotational_target_deg - d.rotational_position_deg))
elif version == 6:  # Z_N_LEGACY_ANGLE
    plot_rotational_tracking_with_pwm(result)
    plot_heading_error(result)

elif version == 7:  # Z_N_LEGACY_DISTANCE
    plot_translational_tracking_with_pwm(result)
    plot_error(result)
    plot_error_speed(result)
    plot_acceleration(result)
elif version == 8:  # Z_N_LEGACY_ANGLE_SPEED
    plot_heading_vs_target_heading(result)
    plot_pwm(result)
    plot_ramp_vs_estimated_speed(result)
    plot_speed_error(result)
    freq, spec, mag = do_fft(result, lambda d: (d.estimated_speed_deg - d.ramp_speed_deg))

    sampling_rate = 1.0/(np.average([d.robot_dt for d in result]))

    index_target = np.argmin(np.abs(freq - 2.0))


    f_osc_index = index_target + np.argmax(mag[index_target:])
    f_osc = freq[f_osc_index]
    ref_sin = np.sin(2 * np.pi * f_osc * np.array([d.dt for d in result]))
    ref_cos = np.cos(2 * np.pi * f_osc * np.array([d.dt for d in result]))
    s = np.array([(d.ramp_speed_deg - d.estimated_speed_deg) for d in result])
    s -= np.mean(s)
    i_component = 2 * s * ref_cos  # In-phase
    q_component = 2 * s * ref_sin  # Quadrature
    # Apply low-pass filter to get amplitude envelope
    from scipy.signal import butter, filtfilt

    from scipy.signal import butter, sosfiltfilt

    sos = butter(2, f_osc * 2 / (sampling_rate / 2), output='sos')
    i_filtered = sosfiltfilt(sos, i_component)
    q_filtered = sosfiltfilt(sos, q_component)

    amplitude_envelope = np.sqrt(i_filtered ** 2 + q_filtered ** 2)
    time = np.array([d.dt for d in result])
    plt.plot(time, s, label="Speed Error")
    plt.plot(time, amplitude_envelope, label="Amplitude Envelope", linewidth=2)
    plt.legend()
    plt.title("Lock-in Demodulated Oscillation Amplitude")
    plt.show(block=True)
    mean_amp = np.mean(amplitude_envelope)
    sigma = np.std(amplitude_envelope)  # you can also set this manually

    weights = np.exp(-((amplitude_envelope - mean_amp) ** 2) / (2 * sigma ** 2))
    weighted_mean = np.sum(weights * amplitude_envelope) / np.sum(weights)
    print(weighted_mean)


elif version == 9:  # Z_N_LEGACY_DISTANCE_SPEED
    plot_translational_tracking(result)
    plot_error_speed(result)
    plot_acceleration(result)
    plot_pwm(result)