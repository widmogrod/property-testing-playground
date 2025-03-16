# Property Testing Playground

[![Pre-commit Checks](https://github.com/widmogrod/property-testing-playground/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/widmogrod/property-testing-playground/actions/workflows/pre-commit.yml)
[![Run Tests](https://github.com/widmogrod/property-testing-playground/actions/workflows/tests.yml/badge.svg)](https://github.com/widmogrod/property-testing-playground/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/widmogrod/property-testing-playground/graph/badge.svg?token=LLKIUXQVW4)](https://codecov.io/github/widmogrod/property-testing-playground)

A demonstration of property-based testing with Python, Hypothesis, and other techniques.


```
uv run pytest
uv run pytest --hypothesis-show-statistics 

uv run pytest --cov --cov-branch

uv run hypothesis write src.reverse

uvx pre-commit run --all-files
```