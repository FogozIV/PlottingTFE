from data import ZieglerNicholsClasses
from data.VersionAndClasses import *
from data.PlottingFunctions import *
from data.CurveBenchmarkClasses import *
from data.ZieglerNicholsClasses import *
from itertools import accumulate
import matplotlib
from math import sqrt
matplotlib.use('QtAgg')

import matplotlib.pyplot as plt
import numpy as np
plt.ion()

version_with_subversion = [4, 10,11]
version_with_subsubversion = [10,11]

version = None
subVersion = None
subsubVersion = None
result = []
class_type = None
#class_type = ZieglerNicholsNotVersionMarkedParser(0,0)
done = True
with open("data_rapport/BenchmarkControllerZieglerNicholsDISTANCE.bin", "rb") as f:
    if class_type is None:
        data = f.read(8)
        if(len(data) != 8):
            raise ValueError("Version of Benchmark not found")
        version = struct.unpack('>Q', data)[0]
        print("Version =", version)
        if(version in version_with_subversion):
            data = f.read(1)
            if(len(data) != 1):
                raise ValueError("Subversion of Benchmark not found")
            subVersion = struct.unpack('>B', data)[0]
            if(version in version_with_subsubversion):
                data = f.read(1)
                if (len(data) != 1):
                    raise ValueError("Subsubversion of Benchmark not found")
                subsubVersion = struct.unpack('>B', data)[0]
                class_type = versions[version]
                if isinstance(class_type, type) and issubclass(class_type, CustomParser):
                    class_type = class_type(subVersion, subsubVersion)
                else:
                    class_type = class_type[subVersion][subsubVersion]
            else:
                print(version, subVersion)
                class_type = versions[version][subVersion]
        else:
            class_type = versions[version]
            if isinstance(class_type, type) and issubclass(class_type, CustomParser):
                class_type = class_type(0,0)
            print(version, subVersion)


    while data := f.read(class_type.get_length()):
        try:
            result.append(class_type.from_bytes(data))
        except ValueError:
            done = False
            print("Value error")
            break
        print(result[-1])
if all(getattr(d, 'dt', 0.0) == 0.0 for d in result):
    dts = list(accumulate(d.robot_dt for d in result))
    for obj, dt in zip(result, dts):
        obj.dt = dt

if not done:
    print("issue")
elif version == 0:
    plot_rotational_tracking(result)
    plot_heading_error(result)
    plot_rotational_speed(result)
    do_fft(result, lambda d: (d.rotational_target_deg - d.rotational_position_deg))

elif version == 1:
    plot_translational_tracking(result)
    plot_error(result)
    plot_error_speed(result)
    plot_acceleration(result)
    do_fft(result, lambda d: (d.translational_target - d.translational_position))

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
elif version == 4:
    plot_translational_tracking(result)
    plot_error(result)
    plot_error_speed(result)
    plot_acceleration(result)
    plot_pwm(result)
    if subVersion == 1:
        plot_up_ui_ud(result)
    elif subVersion == 2 :
        plot_up_ui_ud_uff(result)
    do_fft(result, lambda d: (d.translational_target - d.translational_position))
    do_fft(result, lambda d: (d.ud))
elif version == 6:  # Z_N_LEGACY_ANGLE
    plot_pwm(result)
    plot_speed_error(result)
    plot_pos_target(result)

elif version == 7:  # Z_N_LEGACY_DISTANCE
    plot_translational_tracking_with_pwm(result)
    plot_error(result)
    plot_error_speed(result)
    plot_acceleration(result)
elif version == 8:  # Z_N_LEGACY_ANGLE_SPEED
    plot_heading_vs_target_heading(result)
    plot_pwm(result)
    plot_ramp_vs_estimated_speed(result)
    plot_speed_angle_error(result)
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

elif version == 10:
    #plot_rotational_tracking(result)
    plot_error_speed(result)
    plot_acceleration(result)
    plot_pwm(result)
    plot_up_ui_ud(result)
    plot_robot_dt(result)
    plot_xy_trajectory(result)
    plot_current_error(result)
    if result[0].raw_ud is not None:
        plot_raw_ud_distance(result)
    if result[0].raw_ud_angle is not None:
        plot_raw_ud_angle(result)
    if result[0].a is not None:
        plot_a(result)
elif version == 11:
    #plot_rotational_tracking(result)
    #plot_error_speed(result)
    plot_translational_ramp_speed_comparison(result, other=False)
    plot_acceleration(result)
    plot_pwm(result)
    plot_up_ui_ud(result)
    plot_robot_dt(result)
    plot_xy_trajectory(result)
    plot_current_error(result)
    if result[0].raw_ud is not None:
        plot_raw_ud_distance(result)
    if result[0].raw_ud_angle is not None:
        plot_raw_ud_angle(result)
    if result[0].a is not None:
        plot_a(result)
    plot_variable(result, lambda x: x.rotational_position_deg, ylabel="Rotational Position(deg)", title="Rotational Position in function of time")
    plot_variable(result, lambda x: x.rotational_target_deg, ylabel="Rotational Target(deg)", title="Rotational Target in function of time")
    plot_variable(result, lambda x: x.rotational_target_deg - x.rotational_position_deg)
    plot_rotational_tracking(result)
    plot_translational_tracking(result)
