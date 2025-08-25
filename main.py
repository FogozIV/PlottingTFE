import os

from data import ZieglerNicholsClasses
from data.Parser import CompleteParser, ParsableClass
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
from file_opener import *

#class_type = ZieglerNicholsNotVersionMarkedParser(0,0)

filename = "data_rapport_v2/BenchmarkControllerANGLEESCTuned.bin"

bc_esc_angle = open_file(filename, False)
bc_zn_angle = open_file("data_rapport_v2/BenchmarkControllerANGLEZNTuned.bin", False)

bc_esc_distance = open_file("data_rapport_v2/BenchmarkControllerDistanceFullESC.bin", False)
bc_zn_distance = open_file("data_rapport_v2/BenchmarkControllerDistanceWithoutDFilterAndFF.bin", False)

plt.figure()
plot_variable_fct(bc_esc_angle, lambda x: x.rotational_target - x.rotational_position, ylabel="Rotational Error(deg)", title="Rotational Error in function of time", label="ESC Tuned")
plot_variable_fct(bc_zn_angle, lambda x: x.rotational_target - x.rotational_position, ylabel="Rotational Error(deg)", title="Rotational Error in function of time", label="ZN Tuned")

plt.figure()
plot_variable_fct(bc_zn_distance, lambda x: x.translational_target - x.translational_position, ylabel="Translational Error(mm)", title="Translational Error in function of time", label="ZN Tuned")
plot_variable_fct(bc_esc_distance, lambda x: x.translational_target - x.translational_position, label="ESC Tuned")
plt.show(block=True)

