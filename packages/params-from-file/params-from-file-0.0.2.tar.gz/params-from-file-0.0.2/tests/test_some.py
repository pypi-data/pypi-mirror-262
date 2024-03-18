from params_from_file import params_from_yml


@params_from_yml
def test_1(field_1, field_2, field_3, field_4):
    assert type(field_1) == int
    assert type(field_2) == str
    assert type(field_3) == str
    assert type(field_4) == dict


@params_from_yml
def test_2(field_1, field_2):
    assert type(field_1) == int
    assert type(field_2) == int


def test_without():
    assert 1 == 1
