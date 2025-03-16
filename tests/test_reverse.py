from src.reverse import reverse


def test_reverse() -> None:
    assert reverse([1, 2, 3]) == [3, 2, 1]


# what are problems with this test?
# TODO: group conversation
#
# - code coverage 100%
# - happy path testing. when we write code and then test it, we naturally trust ourselves,
#   and because of that, we
#    - (1) overlook edge cases;
#    - (2) forget that someone in feature can change them, that may make pass, but break behaviour,
#      especially for simpel functions
# - what can be edge cases?
#   - diverse inputs, mutation of list, instead of returning copy, empy list behaviour,...
#     TODO: show example of diverse input, uncomment bad implementation in reverse.py
# - How to get better and avoid those pratfalls?
#   - if we cannot trust implementation, and implementation is black box,
#     then we have to focus on verifying behaviour... but how to doit?
#    - TDD can help, since it forse to start with test first, avoid implementation thingking
#    - Pair programing can help, because every mod 3 iteration, someone is trying to break implementation
#      - mutation testing does that for us automatically
#    - but today, we will learn property testing.
# - what are properties of reverse function?
#   TODO: group conversation
