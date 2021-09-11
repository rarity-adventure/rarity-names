def test_valid_names(names):
    assert names.validate_name("conan")
    assert names.validate_name("Conan")
    assert names.validate_name("Conan the Barbarian")
    assert names.validate_name("abcdefghijklmnopqrstuvw")
    assert names.validate_name("xyz0123456789ABCDEFGHIJ")
    assert names.validate_name("KLMNOPQRSTUVWXYZ")
    assert names.validate_name("this is 25 characters aaa")
    assert names.validate_name("1")


def test_length(names):
    assert not names.validate_name("this is 26 characters aaaa")
    assert not names.validate_name("")


def test_spaces(names):
    assert not names.validate_name("use  two spaces")
    assert not names.validate_name(" leading space")
    assert not names.validate_name("trailing space ")


def test_utf8(names):
    assert not names.validate_name("cönan")
    for s in ".:()=?`![]{}-_,;öäü^'\"":
        assert not names.validate_name(s)


def test_to_lower(names):
    assert names.to_lower("CoNaN tH3 B4rb") == "conan th3 b4rb"
