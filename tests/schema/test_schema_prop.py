from typing import Any
from typing import NoReturn

from hypothesis import given, note, assume, strategies as st

from src.schema.schema import Schema, SPrimitive, SList, PInt, SVariant, PBool, PBit, \
    infer_schema_from_list, merge_schemas


def assert_never(x: NoReturn) -> NoReturn:
    assert False, "Unhandled type: {}".format(type(x).__name__)


@st.composite
def gen_data(draw: st.DrawFn, schema: Schema) -> Any:
    match schema:
        case SPrimitive(p):
            match p:
                case PInt():
                    return draw(st.integers())
                case PBool():
                    return draw(st.booleans())
                case PBit(n):
                    return draw(st.binary(min_size=n // 8, max_size=n // 8))
                case _:
                    assert_never(p)
        case SList(SVariant(variants)):
            return [draw(gen_data(schema=variant)) for variant in variants]
        case SList(s):
            if not s:
                return []

            return [draw(gen_data(schema=s))
                    for _ in range(draw(st.integers(min_value=1, max_value=10)))]
        case SVariant(variants):
            chosen_schema = draw(st.sampled_from(list(variants)))
            return draw(gen_data(schema=chosen_schema))
        case _:
            assert_never(schema)


@st.composite
def gen_schema(draw: st.DrawFn, seed: int = 42, max_depth: int = 3) -> Schema:
    primitive = st.one_of(
        st.builds(PInt),
        st.builds(PBool),
        st.builds(PBit, st.integers(min_value=1, max_value=10).map(lambda x: x * 8))  # forces multiples of 8
    )

    if max_depth <= 0:
        return SPrimitive(draw(primitive))

    return draw(st.one_of(
        st.builds(SPrimitive, primitive),
        st.builds(SList, gen_schema(seed=seed, max_depth=max_depth - 1)),
        st.builds(SVariant,
                  st.builds(frozenset,
                            st.sets(gen_schema(seed=seed, max_depth=max_depth - 1),
                                    min_size=2)))
    ))


@given(schema=gen_schema(), data=st.data())
def test_schema_prop(schema: Schema, data):
    D = [data.draw(gen_data(schema=schema)) for _ in range(10)]
    assume(len(set(map(repr, D))) == 10)
    S1 = infer_schema_from_list(D)
    note(f"schema={schema}")
    note(f"data={D}")
    assert schema == S1

    # Hylomorphism
    # [1,2,3].fold(0, (x, acc) => x + acc)) == 6
    # 6.unfold((x) => ...) == [1,2,3]

@given(schema=gen_schema())
def test_schema_merging_indempotence(schema: Schema):
    assert merge_schemas(schema, schema) == schema

@given(a=gen_schema(), b=gen_schema())
def test_schema_merging_identity(a: Schema, b: Schema):
    assume(a != b)
    assert merge_schemas(a, b) == merge_schemas(b, a)