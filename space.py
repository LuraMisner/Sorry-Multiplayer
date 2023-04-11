from occupied_type import OccupiedType
from reserved_type import ReservedType


class Space:
    def __init__(self):
        self.occupied = OccupiedType.NONE
        self.type = ReservedType.NONE

    def get_occupied(self):
        return self.occupied

    def set_occupied(self, change):
        self.occupied = change

    def get_type(self):
        return self.type

    def set_type(self, enum):
        self.type = enum

    def to_string(self):
        return str(self.occupied) + ', ' + str(self.type)
