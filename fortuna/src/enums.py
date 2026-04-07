import enum
from enum import Enum


class ActionType(Enum):
    PLAY = enum.auto()
    INFO = enum.auto()
    LIST = enum.auto()
    LIST_FIELDS = enum.auto()


class ListType(Enum):
    MEDIA = enum.auto()
    FIELDS = enum.auto()
    FIELD_VALUES = enum.auto()
