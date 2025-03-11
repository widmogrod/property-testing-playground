from typing import List, Any, Set


class PInt:
    pass


class PBit:
    def __init__(self, size):
        self.size = size


class SPrimitive:
    __match_args__ = ("primitive",)

    def __init__(self, primitive: PInt | PBit):
        self.primitive = primitive


class SConflict:
    def __init__(self, conflicts: List["Schema"]):
        self.conflicts = conflicts


class SList:
    __match_args__ = ("of",)

    def __init__(self, of):
        self.of = of


Schema = SList | SPrimitive | SConflict


def infer_schema(data: List[Any]) -> Schema:
    pass
