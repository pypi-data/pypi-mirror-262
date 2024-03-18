import yaml

PARAMS_FROM_YML = "data_driven_yml"


def params_from_yml(func):
    setattr(func, PARAMS_FROM_YML, True)
    return func


def _load_data_yml(filename, params: tuple[str]):
    with open(f"test_data/{filename}.yml", "r") as file:
        data: dict = yaml.safe_load(file)
        test_cases = list(data.keys())
        return (
            ",".join(params),
            [tuple(data[tc][p] for p in params) for tc in test_cases],
            test_cases,
        )


def pytest_generate_tests(metafunc):
    if hasattr(metafunc.definition.function, PARAMS_FROM_YML):
        a, b, c = _load_data_yml(metafunc.definition.name, metafunc.fixturenames)
        metafunc.parametrize(a, b, ids=c)
