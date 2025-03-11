from typing import List, Any, Set

from src.schema.schema import Schema


class Added:
    __match_args__ = ("type",)
    def __init__(self, type: Schema):
        self.type = type

class Removed:
    __match_args__ = ("type",)
    def __init__(self, type: Schema):
        self.type = type

class Unchanged:
    __match_args__ = ("type",)
    def __init__(self, type: Schema):
        self.type = type

class Positional:
    __match_args__ = ("key_or_index",)
    def __init__(self, key_or_index: str | int, type: Schema):
        self.key_or_index = key_or_index
        self.type = type

class Nested:
    __match_args__ = ("set",)
    def __init__(self, set: Set["Diff"]):
        self.set = set

Diff = Added | Removed | Unchanged | Positional | Nested

def compare(schema1: Schema, schema2: Schema) -> Diff:
    pass
