from hypothesis import given, strategies as st

from src.unfold import unfold, fold


def uf(x):
    if x < 1:
        return ([x], None)
    if x % 2 == 0:
        # Even case: output digit is x//2 and next seed is x//2.
        return ([x // 2], x // 2)
    else:
        # Odd case: output digit is (x//2 + x%2) and next seed is x//2.
        return ([x // 2 + x % 2], x // 2)


@given(st.integers())
def test_unfold_prop(x: int):
    L = unfold(x, uf)
    y = fold(L, 0, lambda x, acc: x + acc)
    assert x == y
