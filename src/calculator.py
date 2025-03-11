from typing import Callable


class Add:
    __match_args__ = ("a", "b")

    def __init__(self, a: "CalcDSL", b: "CalcDSL"):
        self.a = a
        self.b = b


class Mul:
    __match_args__ = ("a", "b")

    def __init__(self, a: "CalcDSL", b: "CalcDSL"):
        self.a = a
        self.b = b


class Lit:
    __match_args__ = ("a",)

    def __init__(self, a: int):
        self.a = a


CalcDSL = Add | Mul | Lit
Calculate = Callable[[CalcDSL], int]


def eval(dsl: CalcDSL) -> int:
    match dsl:
        case Lit(a):
            return a
        case Add(a, b):
            # Intentional error to help demonstrate usefulness of property testing
            # return eval(a) * eval(b)
            return eval(a) + eval(b)
        case Mul(a, b):
            return eval(a) * eval(b)
