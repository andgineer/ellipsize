from ellipsize.ellipsize import Dots, ellipsize, ellipsize_format, ellipsize_print


def test_ellipsize():
    a = [1, 2, 3]
    assert ellipsize(a, max_list_items_to_show=10) == a
    assert str(ellipsize(a, max_list_items_to_show=2)) == "[1, 2, ..]"
    assert str(ellipsize(a, max_list_items_to_show=3)) == str(a)
    assert (
        ellipsize({"a": "12345", "b": a}, max_item_length=4, max_list_items_to_show=2)
        == {'a': '1234..', 'b': [1, 2, Dots()]}
    )
    assert (
        str(ellipsize({"a": "12345", "b": a, "c": {"d": a}}, max_item_length=4, max_list_items_to_show=2))
        == "{'a': '1234..', 'b': [1, 2, ..], 'c': {'d': [1, 2, ..]}}"
    )
    assert (
        ellipsize({"a": "12345", "b": a, "c": [{"d": a}, {}, {}]}, max_item_length=4, max_list_items_to_show=2)
        == {'a': '1234..', 'b': [1, 2, Dots()], 'c': [{"d": [1, 2, Dots()]}, {}, Dots()]}
    )


def test_ellipsize_format():
    a = [1, 2, 3]
    assert ellipsize_format(a, max_list_items_to_show=2) == "[1, 2, ..]"


def test_ellipsize_print(capsys):
    a = [1, 2, 3]
    ellipsize_print(a, max_list_items_to_show=2)
    assert capsys.readouterr().out == "[1, 2, ..]\n"
