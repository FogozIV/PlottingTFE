import struct
from dataclasses import dataclass, fields
from typing import Optional, Type
import matplotlib.pyplot as plt
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
        current_figure = plt.gcf()
        plot_variable(results, "up", label="K_p contribution", title="Contributions of each term of the PID controller", ylabel="d.c")
        plot_variable(results, "ui", label="K_i contribution")
        plot_variable(results, "ud", label="K_d contribution")
        plt.figure()
        plot_variable(results, "up", label="K_p contribution", title="Contribution of K_p in d.c.")
        plt.figure()
        plot_variable(results, "ui", label="K_i contribution", title="Contribution of K_i in d.c.")
        plt.figure()
        plot_variable(results, "ud", label="K_d contribution", title="Contribution of K_d in d.c.")
        plt.figure(current_figure)



@dataclass
class ControllerPIDSpeedFeedForward(ControllerPID):
    uff: Optional[float] = None

    @staticmethod
    def display_data(results):
        ControllerPID.display_data(results)
        current_figure = plt.gcf()
        plot_variable(results, "uff", label="Feed forward contribution")
        plt.figure()
        plot_variable(results, "uff", label="Feed forward contribution", title="Contribution of the feed forward in d.c.")
        plt.figure(current_figure)


@dataclass
class ControllerPIDFilteredD(ControllerPID):
    rawUd: Optional[float] = None

    @staticmethod
    def display_data(results):
        ControllerPID.display_data(results)
        current_figure = plt.gcf()
        plot_variable(results, "rawUd", label="Raw K_d contribution")
        plt.figure()
        plot_variable(results, "rawUd", label="Raw K_d contribution", title="Contribution of Raw K_d in d.c.")
        plt.figure(current_figure)

@dataclass
class ControllerFeedForward(Controller):
    innerController: Optional[Controller] = None
    uff: Optional[float] = None
    @staticmethod
    def display_data(results):
        for c in results:
            c.innerController.dt = c.dt
        type(results[0].innerController).display_data([r.innerController for r in results])
        current_figure = plt.gcf()
        plot_variable(results, "uff", label="Feed forward contribution")
        plt.figure()
        plot_variable(results, "uff", label="Feed forward contribution", title="Contribution of the feed forward in d.c.")
        plt.figure(current_figure)

data = [
    Controller,
    ControllerPID,
    ControllerPIDSpeedFeedForward,
    ControllerPIDFilteredD,
    ControllerFeedForward,
]
for d in data:
    controller_types.append(d)