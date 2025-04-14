from src.calculator import Add, Lit, Mul, eval


def test_calculator() -> None:
    assert eval(Add(Lit(2), Lit(2))) == 4, "2 + 2 = 4"
    assert eval(Mul(Lit(2), Lit(2))) == 4, "2 * 2 = 4"
    assert eval(Lit(1)) == 1, "1 = 1"
