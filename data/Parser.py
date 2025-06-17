from typing import Type, TypeVar, List, Generic
import dataclasses
import struct
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