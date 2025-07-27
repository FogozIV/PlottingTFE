from typing import Type, TypeVar, List, Generic
import dataclasses
import struct
import copy
from typing import Any, get_origin, get_args, Union, Optional
import inspect
import matplotlib.pyplot as plt
T = TypeVar('T')
class CustomParser(Generic[T]):
    dataclass_type: Type[T]
    bitmask_function: callable
    def __init__(self, version, subversion):
        self.ALL_FIELDS: List[str] = [f.name for f in dataclasses.fields(self.dataclass_type)]
        self.bitMask = type(self).bitmask_function(version, subversion)
        self.active_fields = [
            field for i, field in enumerate(self.ALL_FIELDS) if self.bitMask & (1 << i)
        ]
        self.field_count = bin(self.bitMask).count("1")

    def get_length(self):
        return self.field_count * 8

    def from_bytes(self, data) -> T:
        if len(data) < self.get_length():
            raise ValueError(
                f'Not enough bytes to unpack {self.__class__.__name__} (need {self.get_length()} bytes)'
            )
        values = struct.unpack(f'>{self.field_count}d', data)
        field_dict = dict(zip(self.active_fields, values))
        return self.dataclass_type(**field_dict)

def set_field_by_path(obj, path: str, value: Any):
    parts = path.split(".")
    for part in parts[:-1]:
        obj = getattr(obj, part)
    setattr(obj, parts[-1], value)

def get_field_by_path(obj, path: str):
    parts = path.split(".")
    for part in parts[:-1]:
        obj = getattr(obj, part)
    return getattr(obj, parts[-1])

def get_all_field_paths(obj, prefix="") -> list[str]:
    paths = []
    for field in dataclasses.fields(obj):
        value = getattr(obj, field.name)
        path = f"{prefix}{field.name}"
        if dataclasses.is_dataclass(value):
            paths.extend(get_all_field_paths(value, prefix=path + "."))
        else:
            paths.append(path)
    return paths



def is_field_subclass_of(field_type, base_class):
    origin = get_origin(field_type)
    args = get_args(field_type)

    # Handle Optional[...], Union[..., None], or plain class
    if origin is Union and args:
        # Check all types in the union except NoneType
        for arg in args:
            if arg is not type(None) and inspect.isclass(arg) and issubclass(arg, base_class):
                return True
        return False
    elif inspect.isclass(field_type) and issubclass(field_type, base_class):
        return True
    return False

def get_static_method_if_possible(field_type, method_name):
    origin = get_origin(field_type)
    args = get_args(field_type)

    # Unwrap Optional[...] / Union[..., None]
    candidates = []
    if origin is Union:
        candidates = [arg for arg in args if arg is not type(None)]
    else:
        candidates = [field_type]

    for candidate in candidates:
        if inspect.isclass(candidate) and issubclass(candidate, ParsableClass):
            method = getattr(candidate, method_name, None)
            if callable(method):
                return method  # not bound, static method
    return None

class ParsableClass:
    def parse(self, f):
        field_paths = get_all_field_paths(self)
        expected_len = 8 * len(field_paths)
        results = []
        while data := f.read(expected_len):
            a = copy.deepcopy(self)
            results.append(a.fill_parsable_from_bytes(data, expected_len, field_paths))
        return results
    def fill_parsable_from_bytes(self, data: bytes, expected_len, field_paths):
        if len(data) < expected_len:
            raise ValueError(f"Expected {expected_len} bytes, got {len(data)}")
        values = struct.unpack(f'>{len(field_paths)}d', data)
        for path, val in zip(field_paths, values):
            set_field_by_path(self, path, val)
        return self
    def update(self):
        pass
    @staticmethod
    def generate(i, data):
        for f in dataclasses.fields(i):
            if is_field_subclass_of(f.type, ParsableClass):
                setattr(i, f.name, get_static_method_if_possible(f.type, "generate")(None, data))
        return i
    @staticmethod
    def display_data(results):
        raise Exception("Not implemented")



class CompleteParser:
    def __init__(self, f, type):
        self.f = f
        self.data_type = type
        self.data_type.generate(self.data_type, self.f)
        self.data_type.update()
        self.results = None

    def get_result(self):
        if self.results is None:
            self.results = self.data_type.parse(self.f)
        return self.results
    def display(self):
        type(self.data_type).display_data(self.get_result())
def plot_variable(results, attr, label=None, ylabel=None, title=None):
    values = [getattr(r, attr, None) for r in results]
    times = [getattr(r, 'dt', 0.0) for r in results]

    if all(v is None for v in values):
        return  # Skip empty

    plt.plot(times, values, label=label or attr)
    plt.xlabel("Time (s)")
    ax = plt.gca()  # get current axes
    title_text = ax.get_title()
    if title:
        plt.title(title)
    elif title_text == "" and attr:
        plt.title(title or attr)

    if ylabel:
        ax.set_ylabel(ylabel)
    elif not ax.get_ylabel() and attr:
        ax.set_ylabel(ylabel or attr)
    if label:
        plt.legend()
    plt.grid(True)

def plot_variable_fct(results, fct, label=None, ylabel=None, title=None):
    values = [fct(r) for r in results]
    times = [getattr(r, 'dt', 0.0) for r in results]
    if all(v is None for v in values):
        return
    plt.plot(times, values, label=label)
    plt.xlabel("Time (s)")
    ax = plt.gca()  # get current axes
    if title:
        plt.title(title)
    if ylabel:
        ax.set_ylabel(ylabel)
    if label:
        plt.legend()
    plt.grid(True)

def show_plots(block=False):
    plt.tight_layout()
    plt.show(block=True)


