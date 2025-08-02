from data.Controllers import Controller
from data.SubControllers import SubController
import struct
from dataclasses import dataclass, fields
from typing import Optional, Type
import copy
from data.Parser import ParsableClass, is_field_subclass_of, plot_variable, show_plots, get_all_field_paths, \
    set_field_by_path, get_field_by_path, plot_variable_fct, plot_2d

import matplotlib.pyplot as plt
import numpy as np
def call_child_end_display(results):
    for c in results:
        c.controller.dt = c.dt
    results = [r.controller for r in results]
    for r in results:
        paths = get_all_field_paths(r)
        for path in paths:
            if issubclass(type(get_field_by_path(r, path)), SubController):
                continue
            set_field_by_path(r, path, get_field_by_path(r, path)/4095)
    type(results[0]).display_data(results)
    show_plots()

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
    controller: Optional[SubController] = None
    @staticmethod
    def display_data(results):
        plt.figure()
        plot_variable(results, "rotational_position", "Position", title="Rotational Position & Target (deg)", ylabel="Position (deg)")
        plot_variable(results, "rotational_target", "Target")
        plt.figure()
        plot_variable(results, "rotational_ramp_speed", "Ramp Speed", title="Angular Speed")
        plot_variable(results, "rotational_estimated_speed", "Estimated Speed", ylabel="Speed (deg/s)")
        #plot_variable(results, "rotational_other_estimated_speed", "Other Estimation")
        plt.figure()
        plot_variable(results, "rotational_ramp_speed", "Ramp Speed", title="Angular Speed with Kalman")
        plot_variable(results, "rotational_estimated_speed", "Estimated Speed", ylabel="Speed (deg/s)")
        plot_variable(results, "rotational_other_estimated_speed", "Other Estimation")
        plt.figure()
        plot_variable(results, "error", "Total Error", title="Total Error Over Time", ylabel="Total Error (deg²)")
        plt.figure()
        plot_variable(results, "currentError", "Current Error", title="Current Error Over Time", ylabel="error² (deg²)")
        plt.figure()
        plot_variable_fct(results, lambda x:x.rotational_target - x.rotational_position, label="Angular error", title="Error in degrees in function of the time", ylabel="Error(deg)")
        plt.figure()
        plot_variable_fct(results, lambda x:x.rotational_position%360-180, label="Angular position", title="Angular position & target in degrees in function of the time", ylabel="Angular Position/Target(deg)")
        plot_variable_fct(results, lambda x:x.rotational_target%360-180, label="Angular target")
        plt.figure()
        call_child_end_display(results)

@dataclass
class BenchmarkDistanceV02(ParsableClass):
    currentError: Optional[float] = None
    error: Optional[float] = None
    dt: Optional[float] = None
    robot_dt: Optional[float] = None
    translational_position: Optional[float] = None
    translational_target: Optional[float] = None
    translational_ramp_speed: Optional[float] = None
    translational_estimated_speed: Optional[float] = None
    translational_other_estimated_speed: Optional[float] = None
    left_motor: Optional[float] = None
    right_motor: Optional[float] = None
    controller: Optional[SubController] = None
    rotational_position: Optional[float] = None
    rotational_target: Optional[float] = None
    currentPositionX: Optional[float] = None
    currentPositionY: Optional[float] = None
    currentPositionAngle: Optional[float] = None
    @staticmethod
    def display_data(results):
        plt.figure()
        plot_variable(results, "error", "Error", title="Cumulative error (mm²)", ylabel="Error(mm²)")
        plt.figure()
        plot_variable(results, "rotational_position", "Position", title="Rotational Position & Target (deg)", ylabel="Position (deg)")
        plot_variable(results, "rotational_target", "Target")
        plt.figure()
        plot_variable(results, "translational_position", "Position", title="Translational Position & Target (mm)", ylabel="Position (mm)")
        plot_variable(results, "translational_target", "Target")
        plt.figure()
        plot_variable(results, "translational_ramp_speed", "Ramp Speed", title="Translational Speed")
        plot_variable(results, "translational_estimated_speed", "Estimated Speed", ylabel="Speed (mm/s)")
        #plot_variable(results, "translational_other_estimated_speed", "Estimated Speed Kalman")
        plt.figure()
        plot_variable(results, "translational_estimated_speed", "Estimated Speed", ylabel="Speed (mm/s)")
        plt.figure()
        plot_variable_fct(results, lambda x:x.translational_target - x.translational_position, label="Translational error", title="Error in mm in function of the time", ylabel="Error(mm)")
        plt.figure()
        call_child_end_display(results)

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
    translational_ramp_speed: Optional[float] = None
    translational_estimated_speed: Optional[float] = None
    translational_other_estimated_speed: Optional[float] = None
    rotational_position: Optional[float] = None
    rotational_target: Optional[float] = None
    rotational_ramp_speed: Optional[float] = None
    rotational_estimated_speed: Optional[float] = None
    rotational_other_estimated_speed: Optional[float] = None
    currentPositionX: Optional[float] = None
    currentPositionY: Optional[float] = None
    leftMotor: Optional[float] = None
    rightMotor: Optional[float] = None
    controllerDistance: Optional[SubController] = None
    controllerAngle: Optional[SubController] = None

@dataclass
class UniversalBenchmarkV01(ParsableClass):
    currentError: Optional[float] = None
    error: Optional[float] = None
    dt: Optional[float] = None
    robot_dt: Optional[float] = None
    currentErrorAngle: Optional[float] = None
    currentErrorDistance: Optional[float] = None
    translational_position: Optional[float] = None
    translational_target: Optional[float] = None
    translational_ramp_speed: Optional[float] = None
    translational_estimated_speed: Optional[float] = None
    translational_other_estimated_speed: Optional[float] = None
    rotational_position: Optional[float] = None
    rotational_target: Optional[float] = None
    rotational_ramp_speed: Optional[float] = None
    rotational_estimated_speed: Optional[float] = None
    rotational_other_estimated_speed: Optional[float] = None
    currentPositionX: Optional[float] = None
    currentPositionY: Optional[float] = None
    currentPositionAngle: Optional[float] = None
    targetPositionX: Optional[float] = None
    targetPositionY: Optional[float] = None
    targetPositionAngle: Optional[float] = None
    leftMotor: Optional[float] = None
    rightMotor: Optional[float] = None
    controller: Optional[Controller] = None
    @staticmethod
    def display_data(results):
        plt.figure()
        plot_variable(results, "rotational_position", "Position", title="Rotational Position & Target (deg)",
                      ylabel="Position (deg)")
        plot_variable(results, "rotational_target", "Target")
        plt.figure()
        plot_variable(results, "rotational_ramp_speed", "Ramp Speed", title="Angular Speed")
        plot_variable(results, "rotational_estimated_speed", "Estimated Speed", ylabel="Speed (deg/s)")
        # plot_variable(results, "rotational_other_estimated_speed", "Other Estimation")
        plt.figure()
        plot_variable(results, "rotational_ramp_speed", "Ramp Speed", title="Angular Speed with Kalman")
        plot_variable(results, "rotational_estimated_speed", "Estimated Speed", ylabel="Speed (deg/s)")
        plot_variable(results, "rotational_other_estimated_speed", "Other Estimation")
        plt.figure()
        plot_variable(results, "error", "Total Error", title="Total Error Over Time", ylabel="Total Error (deg²)")
        plt.figure()
        plot_variable(results, "currentErrorAngle", "Current Error", title="Current Error Over Time", ylabel="error² (deg²)")
        plt.figure()
        plot_variable(results, "currentErrorDistance", "Current Error", title="Current Error Over Time for the distance", ylabel="error² (mm²)")
        plt.figure()
        plot_variable_fct(results, lambda x: x.rotational_target - x.rotational_position, label="Angular error",
                          title="Error in degrees in function of the time", ylabel="Error(deg)")
        plt.figure()
        plot_variable_fct(results, lambda x: x.rotational_position % 360 - 180, label="Angular position",
                          title="Angular position & target in degrees in function of the time",
                          ylabel="Angular Position/Target(deg)")
        plot_variable_fct(results, lambda x: x.rotational_target % 360 - 180, label="Angular target")
        plt.figure()
        plot_variable(results, "translational_position", "Position", title="Translational Position & Target (mm)", ylabel="Position (mm)")
        plot_variable(results, "translational_target", "Target")
        plt.figure()
        plot_variable(results, "translational_ramp_speed", "Ramp Speed", title="Translational Speed")
        plot_variable(results, "translational_estimated_speed", "Estimated Speed", ylabel="Speed (mm/s)")
        #plot_variable(results, "translational_other_estimated_speed", "Estimated Speed Kalman")
        plt.figure()
        plot_variable(results, "translational_ramp_speed", "Ramp Speed", title="Translational Speed")
        plot_variable(results, "translational_estimated_speed", "Estimated Speed", ylabel="Speed (mm/s)")
        plot_variable(results, "translational_other_estimated_speed", "Estimated Speed Kalman")
        plt.figure()
        plot_2d(results, "currentPositionX", "currentPositionY", "Position", title="Current Position", ylabel="Position y (mm)", xlabel="Position x (mm)")

        plt.figure()
        plot_variable(results, "translational_estimated_speed", "Estimated Speed", ylabel="Speed (mm/s)")
        plt.figure()
        plot_variable_fct(results, lambda x:x.translational_target - x.translational_position, label="Translational error", title="Error in mm in function of the time", ylabel="Error(mm)")
        plt.figure()
        call_child_end_display(results)



binaryFileMapForCompleteParser = {
    5: BenchmarkDistanceAngleV01,
    12: BenchmarkAngleV02,
    13: BenchmarkDistanceV02,
    14: UniversalBenchmarkV01,
}