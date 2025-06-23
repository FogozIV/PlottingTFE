import dataclasses
import struct
from gzip import write32u
from itertools import accumulate
from data.Estimator import Estimator
from data.PlottingFunctions import *
from scipy.optimize import curve_fit

import matplotlib
from math import pi
matplotlib.use('QtAgg')

import matplotlib.pyplot as plt
import numpy as np
plt.ion()
@dataclasses.dataclass
class SpeedForwardData:
    estimated_speed: float
    curvilinear_position: float
    robot_dt: float
    dt: float = 0.0
    hand_derivative : float = 0.0
    second_estimated_speed: float = 0.0
    @staticmethod
    def get_length():
        return 3*8

    @staticmethod
    def from_bytes(data: bytes) -> 'SpeedForwardData':
        if len(data) < SpeedForwardData.get_length():
            raise ValueError(f'Not enough bytes to unpack DistancePWMData (need {SpeedForwardData.get_length()} bytes)')
        values = struct.unpack('>3d', data)
        return SpeedForwardData(*values)


result = []
estimator = Estimator(40)
class_type = SpeedForwardData

pwm = 400
w1 = 1 * 2 * pi
w2 = 0.5 * 2 * pi
w3 = 0.25 * 2 * pi

with open("speed_forward.bin", "rb") as f:
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
for i in range(1,len(result)):
    result[i].hand_derivative = (result[i].curvilinear_position - result[i-1].curvilinear_position)/result[i].robot_dt
for i in range(1,len(result)):
    estimator.update(result[i].robot_dt, result[i].curvilinear_position - result[i-1].curvilinear_position)
    result[i].second_estimated_speed = estimator.speed


plot_variable(result, lambda x: x.estimated_speed, "Estimated speed with PLL estimator")
plot_variable(result, lambda x: x.curvilinear_position, "Curvilinear position of the robot")
plot_variable(result, lambda x: x.dt, "time evolution")
plot_variable(result, lambda x: x.hand_derivative, "Raw Numerical derivative")
plot_variable(result, lambda x: x.second_estimated_speed, f"Estimated speed using an offline PLL Estimator of Bandwidth {estimator.bandwidth}")
def model(t, A, tau):
    return A * (1 - np.exp(-t / tau))

initial_guess = [1.0, 1.0]
t_data = [r.dt for r in result]
y_data = [r.hand_derivative for r in result]
params = curve_fit(model, t_data, y_data, p0=initial_guess)
A_fit, tau_fit = params[0]
print(f"Fitted A: {A_fit:.4f}, tau: {tau_fit:.4f}")
c_m = 1/tau_fit
mu_m = A_fit * c_m/pwm
print(f"Fitted c/m: {c_m:.4f}, mu/m: {mu_m:.4f}")
A = w1 + w2 + w3
B = w1*w2 + w1*w3 + w2*w3
C = w1*w2*w3
print(params)
Kd = (A - c_m)/mu_m
Kp = B/mu_m
Ki = C/mu_m

print(f"Found PID : P : {Kp:.4f}, I : {Ki:.4f}, D : {Kd:.4f}")


t_fit = np.linspace(0, 6, 1000)
y_fit = model(t_fit, A_fit, tau_fit)

plt.figure()
plt.scatter(t_data, y_data, label='Data')
plt.plot(t_fit, y_fit, label='Fitted curve', color='red')
plt.xlabel('t')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show(block=True)



