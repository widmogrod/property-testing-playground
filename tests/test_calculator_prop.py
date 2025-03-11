from hypothesis import given, strategies as st

from src.calculator import eval, Add, Mul, Lit, CalcDSL


# Hypothesis strategy to generate random CalcDSL expressions.
# TODO: highlight importance of this function.
# if only thing that we could take from property testing is hypothesis and diverse input generation
# then this is biggest win ever
# TODO: history of one customer with very messy mongoDB data and Stevedore in cratedb
@st.composite
def exprs(draw, max_depth=3):
    if max_depth <= 0:
        # Base case: just a literal integer.
        n = draw(st.integers(min_value=-100, max_value=100))
        return Lit(n)
    else:
        # Randomly choose between a literal, an addition, or a multiplication node.
        strategy = st.one_of(
            st.builds(Lit, st.integers(min_value=-100, max_value=100)),
            st.builds(Add, exprs(max_depth=max_depth - 1), exprs(max_depth=max_depth - 1)),
            st.builds(Mul, exprs(max_depth=max_depth - 1), exprs(max_depth=max_depth - 1))
        )
        return draw(strategy)


# Property test: eval always returns an integer.
@given(expr=exprs())
def test_eval_returns_int(expr: CalcDSL):
    result = eval(expr)
    assert isinstance(result, int)


# Property test: Addition identity.
# For any expression, adding zero should yield the same result.
@given(expr=exprs())
def test_addition_identity(expr: CalcDSL):
    # 0 + 3 = 3
    base_result = eval(expr)
    assert eval(Add(expr, Lit(0))) == base_result
    assert eval(Add(Lit(0), expr)) == base_result


# Property test: Multiplication identity.
# Multiplying by one should yield the same result.
@given(expr=exprs())
def test_multiplication_identity(expr: CalcDSL):
    # 1 * 3 = 3
    base_result = eval(expr)
    assert eval(Mul(expr, Lit(1))) == base_result
    assert eval(Mul(Lit(1), expr)) == base_result


# Property test: Commutativity of addition.
@given(a=exprs(), b=exprs())
def test_add_commutativity(a: CalcDSL, b: CalcDSL):
    # 2 + 3 == 3 + 2
    assert eval(Add(a, b)) == eval(Add(b, a))


# Property test: Commutativity of multiplication.
@given(a=exprs(), b=exprs())
def test_mul_commutativity(a: CalcDSL, b: CalcDSL):
    # 2 * 3 == 3 * 2
    assert eval(Mul(a, b)) == eval(Mul(b, a))


# Property test: Associativity of addition.
@given(a=exprs(), b=exprs(), c=exprs())
def test_add_associativity(a: CalcDSL, b: CalcDSL, c: CalcDSL):
    # (2 + 3) + 4 == 2 + (3 + 4)
    assert eval(Add(Add(a, b), c)) == eval(Add(a, Add(b, c)))


# Property test: Associativity of multiplication.
@given(a=exprs(), b=exprs(), c=exprs())
def test_mul_associativity(a: CalcDSL, b: CalcDSL, c: CalcDSL):
    # (2 * 3) * 4 == 2 * (3 * 4)
    assert eval(Mul(Mul(a, b), c)) == eval(Mul(a, Mul(b, c)))
