import pytest

from ellipsize.ellipsize import Dots, ellipsize, format_ellipsized, print_ellipsized


def test_ellipsize():
    a = [1, 2, 3]
    assert ellipsize(a, max_items_to_show=10) == a
    assert str(ellipsize(a, max_items_to_show=2)) == "[1, 2, ..]"
    assert str(ellipsize(a, max_items_to_show=3)) == str(a)
    assert ellipsize({"a": "12345", "b": a}, max_item_length=4, max_items_to_show=2) == {
        "a": "1234..",
        "b": [1, 2, Dots()],
    }
    result = ellipsize(
        {"a": "12345", "b": a, "c": {"d": a}}, max_item_length=4, max_items_to_show=2
    )
    assert len(result) == 3  # 2 items + ".."
    assert result["a"] == "1234.."
    assert result["b"] == [1, 2, Dots()]
    assert ".." in result
    result2 = ellipsize(
        {"a": "12345", "b": a, "c": [{"d": a}, {}, {}]}, max_item_length=4, max_items_to_show=2
    )
    assert len(result2) == 3  # 2 items + ".."
    assert result2["a"] == "1234.."
    assert result2["b"] == [1, 2, Dots()]
    assert ".." in result2


def test_format_ellipsized():
    a = [1, 2, 3]
    assert format_ellipsized(a, max_items_to_show=2) == "[1, 2, ..]"


def test_dict_ellipsize():
    large_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
    result = ellipsize(large_dict, max_items_to_show=3)
    assert len(result) == 4  # 3 items + ".."
    assert ".." in result
    assert isinstance(result[".."], Dots)
    assert result["a"] == 1
    assert result["b"] == 2
    assert result["c"] == 3

    # Test empty dict
    assert ellipsize({}) == {}

    # Test nested dict truncation
    nested = {"x": {"a": 1, "b": 2, "c": 3}, "y": 2}
    result = ellipsize(nested, max_items_to_show=2)
    assert len(result["x"]) == 3  # 2 items + ".."
    assert ".." in result["x"]
    assert isinstance(result["x"][".."], Dots)


def test_tuple_ellipsize():
    large_tuple = (1, 2, 3, 4, 5)
    result = ellipsize(large_tuple, max_items_to_show=3)
    assert result == (1, 2, 3, Dots())
    assert isinstance(result, tuple)

    # Test empty tuple
    assert ellipsize(()) == ()

    # Test nested tuple
    nested = ([1, 2, 3], (4, 5, 6, 7))
    result = ellipsize(nested, max_items_to_show=2)
    assert result == ([1, 2, Dots()], (4, 5, Dots()))


def test_max_items_to_show_zero():
    # zero means show nothing, but still append Dots for non-empty collections
    assert ellipsize([1, 2, 3], max_items_to_show=0) == [Dots()]
    assert ellipsize((1, 2, 3), max_items_to_show=0) == (Dots(),)
    result = ellipsize({"a": 1, "b": 2}, max_items_to_show=0)
    assert list(result.keys()) == [".."]
    assert isinstance(result[".."], Dots)


def test_max_items_to_show_exact_boundary():
    # list length == max_items_to_show: no Dots appended
    assert ellipsize([1, 2, 3], max_items_to_show=3) == [1, 2, 3]
    assert ellipsize([1, 2, 3], max_items_to_show=4) == [1, 2, 3]


def test_max_item_length_boundary():
    # string exactly at the limit: no ".." appended
    assert ellipsize("abcde", max_item_length=5) == "abcde"
    # one char over: truncate + ".."
    assert ellipsize("abcdef", max_item_length=5) == "abcde.."


def test_dot_dot_key_in_dict():
    # if the dict already has ".." as a key and gets truncated,
    # the ellipsis marker overwrites the original ".." value
    obj = {"..": "original", "a": 1, "b": 2}
    result = ellipsize(obj, max_items_to_show=1)
    assert isinstance(result[".."], Dots)


def test_custom_object_repr_truncation():
    class BigObj:
        def __repr__(self) -> str:
            return "x" * 20

    result = ellipsize(BigObj(), max_item_length=5)
    assert result == "xxxxx.."


def test_invalid_params():
    with pytest.raises(ValueError):
        ellipsize([1, 2], max_items_to_show=-1)
    with pytest.raises(ValueError):
        ellipsize([1, 2], max_item_length=-1)
    with pytest.raises(ValueError):
        ellipsize([1, 2], max_items_to_show=1.5)  # type: ignore[arg-type]


def test_set_converted_to_string():
    # sets are not handled as collections, so they become strings
    result = ellipsize({1, 2, 3})
    assert isinstance(result, str)


def test_print_ellipsized(capsys):
    a = [1, 2, 3]
    print_ellipsized(a, max_items_to_show=2)
    assert capsys.readouterr().out == "[1, 2, ..]\n"

    print_ellipsized(a, "2nd", max_items_to_show=2, end="", sep="?")
    assert capsys.readouterr().out == "[1, 2, ..]?'2nd'"
