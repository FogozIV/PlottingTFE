import struct
from dataclasses import dataclass, fields
from typing import Optional, Type
import copy
from data.Parser import ParsableClass, plot_variable, show_plots, get_all_field_paths, set_field_by_path, \
    get_field_by_path

controller_types = [
]
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
class ControllerPID(Controller):
    up: Optional[float] = None
    ui: Optional[float] = None
    ud: Optional[float] = None

    @staticmethod
    def display_data(results):
        Controller.display_data(results)
        plot_variable(results, "up", label="K_p contribution")
        plot_variable(results, "ui", label="K_i contribution")
        plot_variable(results, "ud", label="K_d contribution")


@dataclass
class ControllerPIDSpeedFeedForward(ControllerPID):
    uff: Optional[float] = None

    @staticmethod
    def display_data(results):
        ControllerPID.display_data(results)
        plot_variable(results, "uff", label="Feed forward contribution")


@dataclass
class ControllerPIDFilteredD(ControllerPID):
    rawUd: Optional[float] = None

    @staticmethod
    def display_data(results):
        ControllerPID.display_data(results)
        plot_variable(results, "rawUd", label="Raw K_d contribution")

@dataclass
class ControllerFeedForward(Controller):
    innerController: Optional[Controller] = None
    uff: Optional[float] = None
    @staticmethod
    def display_data(results):
        for c in results:
            c.innerController.dt = c.dt
        type(results[0].innerController).display_data([r.innerController for r in results])
        plot_variable(results, "uff", label="Feed forward contribution")

data = [
    Controller,
    ControllerPID,
    ControllerPIDSpeedFeedForward,
    ControllerPIDFilteredD,
    ControllerFeedForward,
]
for d in data:
    controller_types.append(d)