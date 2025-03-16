from src.unfold import unfold, fold


from typing import Optional


def uf(x: int) -> tuple[list[int], Optional[int]]:
    if x <= 1:
        return ([x], None)
    if x % 2 == 0:
        # Even case: output digit is x//2 and next seed is x//2.
        return ([x // 2], x // 2)
    else:
        # Odd case: output digit is (x//2 + x%2) and next seed is x//2.
        return ([x // 2 + x % 2], x // 2)


def test_unfold() -> None:
    assert unfold(6, uf) == [1, 2, 3]
    assert fold([1, 2, 3], 0, lambda x, acc: x + acc) == 6


def test_unfold_2() -> None:
    I1 = 6
    L = unfold(I1, uf)
    I2 = fold(L, 0, lambda x, acc: x + acc)
    assert I1 == I2

    # TODO this structure has a name. Hylomorphism
