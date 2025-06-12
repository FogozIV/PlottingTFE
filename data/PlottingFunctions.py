import matplotlib.pyplot as plt
import numpy as np
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
def plot_current_error(data):
    if not data:
        print("No data to plot.")
        return

    time = [d.dt for d in data]
    current_errors = [d.current_error for d in data]

    plt.figure()
    plt.plot(time, current_errors, label="Error |mm|")
    plt.xlabel("Time (s)")
    plt.ylabel("Error")
    plt.title("Evolution of the Error Over Time")
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
    time = [d.dt for d in data]
    plt.plot(time, [d.left_pwm for d in data], label="Left PWM")
    plt.plot(time, [d.right_pwm for d in data], label="Right PWM")
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
def plot_up_ui_ud(data):
    if not data:
        print("No data to plot.")
        return
    time = [d.dt for d in data]
    plt.figure()
    plt.plot(time, [d.up for d in data], label="UP")
    plt.plot(time, [d.ui for d in data], label="UI")
    plt.plot(time, [d.ud for d in data], label="UD")
    plt.title("PWM result")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)
def plot_xy_trajectory(data):
    if not data:
        print("No data to plot.")
        return

    actual_x = [d.x for d in data]
    actual_y = [d.y for d in data]
    target_x = [d.target_x for d in data]
    target_y = [d.target_y for d in data]

    plt.figure()
    plt.plot(actual_x, actual_y, label="Actual Path")
    plt.plot(target_x, target_y, label="Target Path")
    plt.xlabel("X position (mm)")
    plt.ylabel("Y position (mm)")
    plt.title("2D Trajectory Tracking")
    plt.legend()
    plt.axis('equal')  # Ensure aspect ratio is correct
    plt.grid(True)
    plt.tight_layout()
    plt.show(block=True)