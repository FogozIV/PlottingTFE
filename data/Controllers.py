import struct
from dataclasses import dataclass, fields
from typing import Optional, Type
import matplotlib.pyplot as plt
import copy
from data.Parser import ParsableClass, plot_variable, show_plots, get_all_field_paths, set_field_by_path, \
    get_field_by_path
from data.SubControllers import SubController

controller_types = []

@dataclass
class Controller(ParsableClass):
    def has_inner(self):
        return "innerController" in {f.name for f in fields(self)}

    @staticmethod
    def generate(i, data):
        if i is not None:
            raise Exception("unknown state")
        controller_type = struct.unpack(">B", data.read(1))[0]
        a = controller_types[controller_type]()
        return ParsableClass.generate(a, data)

    @staticmethod
    def display_data(results):
        pass

@dataclass
class TripleBasicController(ParsableClass):
    distance_controller: Optional[SubController] = None
    angle_controller: Optional[SubController] = None
    distance_angle_controller: Optional[SubController] = None
    @staticmethod
    def display_data(results):
        for c in results:
            c.distance_controller.dt = c.dt
            c.angle_controller.dt = c.dt
            c.distance_angle_controller.dt = c.dt
        type(results[0].distance_controller).show([r.distance_controller for r in results], "distance controller")
        plt.figure()
        type(results[0].angle_controller).show([r.angle_controller for r in results], "angle controller")
        plt.figure()
        type(results[0].distance_angle_controller).show([r.distance_angle_controller for r in results], "distance angle controller")

data = [
    Controller,
    TripleBasicController,
]
for d in data:
    controller_types.append(d)