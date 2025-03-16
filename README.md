# Property Testing Playground

[![Pre-commit Checks](https://github.com/widmogrod/property-testing-playground/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/widmogrod/property-testing-playground/actions/workflows/pre-commit.yml)
[![Run Tests](https://github.com/widmogrod/property-testing-playground/actions/workflows/tests.yml/badge.svg)](https://github.com/widmogrod/property-testing-playground/actions/workflows/tests.yml)

A demonstration of property-based testing with Python, Hypothesis, and other techniques.


```
uv run pytest
uv run pytest --hypothesis-show-statistics 

uv run pytest --cov --cov-branch

uv run hypothesis write src.reverse

uvx pre-commit run --all-files
```