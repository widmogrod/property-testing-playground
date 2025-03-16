# mypy: disable-error-code="misc"
from typing import Any
from typing import NoReturn

from hypothesis import given, note, assume, strategies as st
from pytest import raises as rises

from src.schema.schema import (
    Schema,
    SPrimitive,
    SList,
    PInt,
    SVariant,
    PBool,
    PBit,
    infer_schema_from_list,
    merge_schemas,
    infer_schema_from_one,
)


def assert_never(x: NoReturn) -> NoReturn:
    assert False, "Unhandled type: {}".format(type(x).__name__)


@st.composite
def gen_not_implemented_data(draw: st.DrawFn, max_depth: int = 3) -> Any:
    base = st.one_of(
        st.none(),
        # st.integers(),
        # st.booleans(),
        # st.binary(min_size=1, max_size=10),
        st.floats(allow_nan=False, allow_infinity=False),
        st.decimals(allow_nan=False, allow_infinity=False),
        st.text(),
        st.dates(),
    )

    recursive_lists = st.recursive(
        base,
        lambda children: st.lists(children, min_size=1, max_size=5),
        max_leaves=max_depth,
    )

    recursive_dicts = st.recursive(
        st.dictionaries(st.text(), base),
        lambda children: st.dictionaries(st.text(), children),
        max_leaves=max_depth,
    )

    return draw(st.one_of(base, recursive_lists, recursive_dicts))


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

            return [
                draw(gen_data(schema=s))
                for _ in range(draw(st.integers(min_value=1, max_value=10)))
            ]
        case SVariant(variants):
            chosen_schema = draw(st.sampled_from(list(variants)))
            return draw(gen_data(schema=chosen_schema))
        case _:
            assert_never(schema)


MAX_DEPTH = 5


@st.composite
def gen_schema(draw: st.DrawFn, max_depth: int = MAX_DEPTH) -> Schema:
    primitive = st.one_of(
        st.builds(PInt),
        st.builds(PBool),
        st.builds(
            PBit, st.integers(min_value=1, max_value=10).map(lambda x: x * 8)
        ),  # forces multiples of 8
    )

    if max_depth <= 0:
        return SPrimitive(draw(primitive))

    # max_depth < MAX_DEPTH:
    #  Variant type cannot be on the top level,
    #   because then hypothesis can go into generating only one flavour of data
    #   and purpose of this function is to generate data that represent complete schema definition
    # max_depth % 2 == 0:
    #  Variant(1, 2) === Variant(Variant(1,2))
    #   semantic this is equal
    #   but __eq__ treat those values as different
    #   generating variants every second level will help to avoid need of searching for other solutions
    if max_depth < MAX_DEPTH and max_depth % 2 == 0:
        variant_result: Schema = draw(gen_schema_variant(max_depth=max_depth))
        return variant_result

    other_result: Schema = draw(
        st.one_of(
            st.builds(SPrimitive, primitive),
            st.builds(SList, gen_schema(max_depth=max_depth - 1)),
            st.builds(SList, st.just(None)),
        )
    )
    return other_result


@st.composite
def gen_schema_variant(draw: st.DrawFn, max_depth: int = 2) -> Schema:
    result: Schema = draw(
        st.builds(
            SVariant,
            st.builds(
                frozenset[Schema],
                st.sets(gen_schema(max_depth=max_depth - 1), min_size=2),
            ),
        )
    )
    return result


@given(schema=gen_schema(), data=st.data())
def test_if_schema_inference_works(schema: Schema, data: st.DataObject) -> None:
    D = [data.draw(gen_data(schema=schema)) for _ in range(10)]
    S1 = infer_schema_from_list(D)
    note(f"schema={schema}")
    note(f"data={D}")
    assert schema == S1

    # Hylomorphism
    # [1,2,3].fold(0, (x, acc) => x + acc)) == 6
    # 6.unfold((x) => ...) == [1,2,3]


@given(schema=gen_schema())
def test_if_merging_is_invariance(schema: Schema) -> None:
    assert merge_schemas(schema, schema) == schema


@given(a=gen_schema(), b=gen_schema())
def test_if_schema_merging_is_commutative(a: Schema, b: Schema) -> None:
    assume(a != b)
    assert merge_schemas(a, b) == merge_schemas(b, a)


# @example(data=0.0).xfail(raises=ValueError)
# @example(data=None).xfail(raises=ValueError)
@given(data=gen_not_implemented_data())
def test_that_infer_schema_fails_on_unknown_data(data: Any) -> None:
    with rises(ValueError):
        infer_schema_from_one(data)


@given(variant=gen_schema_variant(), data=st.data())
def test_variant_generation(variant: SVariant, data: st.DataObject) -> None:
    assume(len(variant.variants) >= 2)
    D1 = data.draw(gen_data(schema=variant))
    D2 = data.draw(gen_data(schema=variant))
    assume(D1 != D2)
    assert D1 != D2
