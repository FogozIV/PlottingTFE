from data.Controllers import Controller
import struct
from dataclasses import dataclass, fields
from typing import Optional, Type
import copy
from data.Parser import ParsableClass, is_field_subclass_of, plot_variable, show_plots, get_all_field_paths, \
    set_field_by_path, get_field_by_path, plot_variable_fct

import matplotlib.pyplot as plt
import numpy as np

@dataclass
class BenchmarkAngleV02(ParsableClass):
    currentError: Optional[float] = None
    error: Optional[float] = None
    dt: Optional[float] = None
    robot_dt: Optional[float] = None
    rotational_target: Optional[float] = None
    rotational_position: Optional[float] = None
    rotational_ramp_speed: Optional[float] = None
    rotational_estimated_speed: Optional[float] = None
    rotational_other_estimated_speed: Optional[float] = None
    left_motor: Optional[float] = None
    right_motor: Optional[float] = None
    controller: Optional[Controller] = None
    @staticmethod
    def display_data(results):
        plt.figure()
        plot_variable(results, "rotational_position", "Position")
        plot_variable(results, "rotational_target", "Target")
        plt.figure()
        plot_variable(results, "rotational_ramp_speed", "Ramp Speed")
        plot_variable(results, "rotational_estimated_speed", "Estimated Speed")
        #plot_variable(results, "rotational_other_estimated_speed", "Other Estimation")
        plt.figure()
        plot_variable(results, "error", "Total Error", title="Total Error Over Time")
        plt.figure()
        plot_variable(results, "currentError", "Current Error")
        plt.figure()
        plot_variable_fct(results, lambda x:x.rotational_target - x.rotational_position, label="Angular error", title="Error in degrees in function of the time", ylabel="Error(deg)")
        plt.figure()
        plot_variable_fct(results, lambda x:x.rotational_position%360-180)
        plot_variable_fct(results, lambda x:x.rotational_target%360-180)
        plt.figure()
        for c in results:
            c.controller.dt = c.dt
        results = [r.controller for r in results]
        print(results)
        for r in results:
            paths = get_all_field_paths(r)
            for path in paths:
                if issubclass(type(get_field_by_path(r, path)),Controller):
                    continue
                set_field_by_path(r, path, get_field_by_path(r, path)/4095)
        type(results[0]).display_data(results)
        show_plots()

@dataclass
class BenchmarkDistanceV02(ParsableClass):
    currentError: Optional[float] = None
    error: Optional[float] = None
    dt: Optional[float] = None
    robot_dt: Optional[float] = None
    translational_position: Optional[float] = None
    translational_target: Optional[float] = None
    left_motor: Optional[float] = None
    right_motor: Optional[float] = None
    controller: Optional[Controller] = None
    rotational_position: Optional[float] = None
    rotational_target: Optional[float] = None
    currentPositionX: Optional[float] = None
    currentPositionY: Optional[float] = None
    currentPositionAngle: Optional[float] = None

@dataclass
class BenchmarkDistanceAngleV01(ParsableClass):
    currentError: Optional[float] = None
    error: Optional[float] = None
    dt: Optional[float] = None
    robot_dt: Optional[float] = None
    currentErrorAngle: Optional[float] = None
    currentErrorDistance: Optional[float] = None
    translational_position: Optional[float] = None
    translational_target: Optional[float] = None
    rotational_position: Optional[float] = None
    rotational_target: Optional[float] = None
    currentPositionX: Optional[float] = None
    currentPositionY: Optional[float] = None
    leftMotor: Optional[float] = None
    rightMotor: Optional[float] = None
    controllerDistance: Optional[Controller] = None
    controllerAngle: Optional[Controller] = None


binaryFileMapForCompleteParser = {
    5: BenchmarkDistanceAngleV01,
    12: BenchmarkAngleV02,
    13: BenchmarkDistanceV02,
}