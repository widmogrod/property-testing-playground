from typing import TypeVar, Callable, Tuple, List, Optional

A = TypeVar("A")
B = TypeVar("B")


def unfold(seed: A, f: Callable[[A], Tuple[List[B], Optional[A]]]) -> List[B]:
    result = []
    current: Optional[A] = seed
    # Continue until the seed becomes None
    while current is not None:
        digits, current = f(current)
        result.extend(digits)

    return result[::-1]


def fold(xs: List[B], result: A, f: Callable[[B, A], A]) -> A:
    for x in xs:
        result = f(x, result)
    return result
