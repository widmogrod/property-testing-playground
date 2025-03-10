from typing import Any, Callable, List

import pytest
from hypothesis import given, strategies as st

from src.reverse import reverse

# Define the higher-order type
Reversible = Callable[[List[Any]], List[Any]]

@pytest.mark.parametrize(
    "reversible",
    [
        reverse,
    ],
)
def test_spec_reversible_func(reversible: Reversible):
    @given(st.lists(st.integers()), st.lists(st.integers()))
    def give_properties(input: List[Any], input2: List[Any]):
        assert (
                reversible(reversible(input)) == input
        ), "reversing twice must result in original"
        assert len(reversible(input)) == len(input), "reverse preserve length of list"
        assert set(reversible(input)) == set(input), "reverse preserve elements"

        assert reversible(input + input2) == reversible(input2) + reversible(input), (
            "reverse of concatenation of list "
            "is the same as concatenation of reversed lists"
        )

        if len(input) > 0:
            assert reversible(input)[0] == input[-1], "first becomes last"
            assert reversible(input)[-1] == input[0], "last becomes first"

    give_properties()

    def symetry_property(list: List[Any]):
        assert reversible(list) == list, "reverse of symmetric lists must be symmetric"

    empty_list: List[Any] = []
    single_element_list: List[Any] = [1]

    symetry_property(empty_list)
    symetry_property(single_element_list)
