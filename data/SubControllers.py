import struct
from dataclasses import dataclass, fields
from typing import Optional, Type
import matplotlib.pyplot as plt
import copy
from data.Parser import ParsableClass, plot_variable, show_plots, get_all_field_paths, set_field_by_path, \
    get_field_by_path

sub_controller_types = [
]
@dataclass
class SubController(ParsableClass):
    def has_inner(self):
        return "innerSubController" in {f.name for f in fields(self)}

    @staticmethod
    def generate(i, data):
        if i is not None:
            raise Exception("unknown state")
        controller_type = struct.unpack(">B", data.read(1))[0]
        a = sub_controller_types[controller_type]()
        return ParsableClass.generate(a, data)

    @staticmethod
    def display_data(results):
        SubController.show(results)
    @staticmethod
    def show(results, str=""):
        raise Exception("Not implemented")


@dataclass
class SubControllerPID(SubController):
    up: Optional[float] = None
    ui: Optional[float] = None
    ud: Optional[float] = None

    @staticmethod
    def display_data(results):
        SubControllerPID.show(results)
    @staticmethod
    def show(results, str=""):
        current_figure = plt.gcf()
        plot_variable(results, "up", label="K_p contribution", title=f"Contributions of each term of the PID {str if str!= "" else "controller"}", ylabel="d.c")
        plot_variable(results, "ui", label="K_i contribution")
        plot_variable(results, "ud", label="K_d contribution")
        plt.figure()
        plot_variable(results, "up", label="K_p contribution", title=f"Contribution of K_p in d.c. {("for the " + str) if str != "" else ""}")
        plt.figure()
        plot_variable(results, "ui", label="K_i contribution", title=f"Contribution of K_i in d.c. {("for the " + str) if str != "" else ""}")
        plt.figure()
        plot_variable(results, "ud", label="K_d contribution", title=f"Contribution of K_d in d.c. {("for the " + str) if str != "" else ""}")
        plt.figure(current_figure)



@dataclass
class SubControllerPIDSpeedFeedForward(SubControllerPID):
    uff: Optional[float] = None

    @staticmethod
    def display_data(results):
        SubControllerPIDSpeedFeedForward.show(results)
    @staticmethod
    def show(results, str=""):
        SubControllerPID.show(results, str)
        current_figure = plt.gcf()
        plot_variable(results, "uff", label="Feed forward contribution")
        plt.figure()
        plot_variable(results, "uff", label="Feed forward contribution", title=f"Contribution of the feed forward in d.c. {("for the " + str) if str != "" else ""}")
        plt.figure(current_figure)


@dataclass
class SubControllerPIDFilteredD(SubControllerPID):
    rawUd: Optional[float] = None

    @staticmethod
    def display_data(results):
        SubControllerPIDFilteredD.show(results)
    @staticmethod
    def show(results, str=""):
        SubControllerPID.show(results, str)
        current_figure = plt.gcf()
        plot_variable(results, "rawUd", label="Raw K_d contribution")
        plt.figure()
        plot_variable(results, "rawUd", label="Raw K_d contribution", title=f"Contribution of Raw K_d in d.c. {("for the " + str) if str != "" else ""}")
        plt.figure(current_figure)

@dataclass
class SubControllerFeedForward(SubController):
    innerSubController: Optional[SubController] = None
    uff: Optional[float] = None
    @staticmethod
    def display_data(results):
        SubControllerFeedForward.show(results)
    @staticmethod
    def show(results, str=""):
        for c in results:
            c.innerSubController.dt = c.dt
        type(results[0].innerSubController).show([r.innerSubController for r in results], str)
        current_figure = plt.gcf()
        plot_variable(results, "uff", label="Feed forward contribution")
        plt.figure()
        plot_variable(results, "uff", label="Feed forward contribution", title=f"Contribution of the feed forward in d.c. {("for the " + str) if str != "" else ""}")
        plt.figure(current_figure)



data = [
    SubController,
    SubControllerPID,
    SubControllerPIDSpeedFeedForward,
    SubControllerPIDFilteredD,
    SubControllerFeedForward,
]
for d in data:
    sub_controller_types.append(d)