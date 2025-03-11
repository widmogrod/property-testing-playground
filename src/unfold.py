from typing import TypeVar, Callable, Tuple, List

A = TypeVar("A")
B = TypeVar("B")


def unfold(seed: A, f: Callable[[A], Tuple[List[B], A | None]]) -> List[B]:
    result = []
    # Continue until the seed becomes 0 (or any falsy value)
    while seed:
        digits, seed = f(seed)
        result.extend(digits)

    return result[::-1]

def fold(xs: List[B], result: A, f: Callable[[B, A], A]) -> A:
    for x in xs:
        result = f(x, result)
    return result