# Setup
in conftest.py
```python
pytest_plugins = ["parametrize_from_file.generate_tests"]
```

# Usage

## Code
from parametrize_from_file import params_from_yml

```python
@params_from_yml
def test_first(string):
    assert len(string) > 0

@params_from_yml
def test_second(numer_1, number_2):
    assert number_1 > number_2
```

## Data Files
test_data/test_first.yml
```yml
tc_not_zero_1:
    string: some text
tc_not_zero_2:
    string: another text
tc_not_zero_3:
    string: still text
```

test_data/test_second.yml
```yml
tc_compare_1:
    number_1: 4
    number_2: 5
tc_compare_2:
    number_1: 7
    number_2: 5
```