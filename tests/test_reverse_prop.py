from typing import Any, List

from hypothesis import given, strategies as st

from src.reverse import reverse


@given(st.lists(st.integers()))
def test_reverse_twice(input: List[Any]):
    assert reverse(reverse(input)) == input, "reversing twice must result in original"


@given(st.lists(st.integers()))
def test_reverse_preserves_length(input: List[Any]):
    assert len(reverse(input)) == len(input), "reverse preserve length of list"


@given(st.lists(st.integers()))
def test_reverse_preserves_elements(input: List[Any]):
    assert set(reverse(input)) == set(input), "reverse preserve elements"


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_reverse_concatenation_property(input: List[Any], input2: List[Any]):
    assert reverse(input + input2) == reverse(input2) + reverse(input), (
        "reverse of concatenation of list "
        "is the same as concatenation of reversed lists"
    )


@given(st.lists(st.integers(), min_size=1))
def test_reverse_first_last_elements(input: List[Any]):
    assert reverse(input)[0] == input[-1], "first becomes last"
    assert reverse(input)[-1] == input[0], "last becomes first"


def test_symetry_property():
    def symetry_property(list: List[Any]):
        assert reverse(list) == list, "reverse of symmetric lists must be symmetric"

    empty_list: List[Any] = []
    single_element_list: List[Any] = [1]

    symetry_property(empty_list)
    symetry_property(single_element_list)
