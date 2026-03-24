"""Visualize huge Python objects as nicely reduced strings."""

from pprint import pformat
from typing import Any, Hashable, Union

EllipsizedValue = Union[
    int,
    float,
    str,
    list["EllipsizedValue"],
    tuple["EllipsizedValue", ...],
    dict[Hashable, "EllipsizedValue"],
    "Dots",
]


class Dots(dict):  # type: ignore[misc]
    """Show dots inside Python objects repr."""

    def __repr__(self) -> str:
        """Show dots."""
        return ".."


def ellipsize(
    obj: object,
    max_items_to_show: int = 10,
    max_item_length: int = 1024,
) -> EllipsizedValue:
    """Reduce huge list/dict to show on screen.

    In lists (including dict items) show only 1st `max_items_to_show`
    and add ".." if there is more.
    Limit max dict/list length at max_item_length.

    Args:
        obj: Python object to ellipsize
        max_items_to_show: if List or Dict in obj (including nested) has more items,
            then show ".." instead of the rest items
        max_item_length: if List's or Dict's item are not another List/Dict
            and its string representation is longer, show ".." instead of the rest of it
    """
    if not isinstance(max_items_to_show, int) or max_items_to_show < 0:
        raise ValueError(f"max_items_to_show must be a non-negative int, got {max_items_to_show!r}")
    if not isinstance(max_item_length, int) or max_item_length < 0:
        raise ValueError(f"max_item_length must be a non-negative int, got {max_item_length!r}")

    if isinstance(obj, (int, float)):
        return obj

    # Handle empty collections
    if isinstance(obj, (list, tuple, dict)) and len(obj) == 0:
        return obj

    # Handle non-empty collections
    if isinstance(obj, list):
        return _ellipsize_list(obj, max_items_to_show, max_item_length)
    if isinstance(obj, tuple):
        return tuple(_ellipsize_list(list(obj), max_items_to_show, max_item_length))
    if isinstance(obj, dict):
        return _ellipsize_dict(obj, max_items_to_show, max_item_length)

    s = str(obj)
    suffix = ".." if len(s) > max_item_length else ""
    return s[:max_item_length] + suffix


def _ellipsize_list(
    obj: list[object],
    max_items_to_show: int,
    max_item_length: int,
) -> list[EllipsizedValue]:
    """Ellipsize list."""
    result_list = [
        ellipsize(
            val,
            max_items_to_show=max_items_to_show,
            max_item_length=max_item_length,
        )
        for val in obj[:max_items_to_show]
    ]
    if len(obj) > max_items_to_show:
        result_list.append(Dots())
    return result_list


def _ellipsize_dict(
    obj: dict[object, object],
    max_items_to_show: int,
    max_item_length: int,
) -> dict[Hashable, EllipsizedValue]:
    """Ellipsize dict."""
    items = list(obj.items())[:max_items_to_show]
    result_dict: dict[Hashable, EllipsizedValue] = {
        key: ellipsize(
            val,
            max_items_to_show=max_items_to_show,
            max_item_length=max_item_length,
        )
        for key, val in items
    }
    if len(obj) > max_items_to_show:
        result_dict[".."] = Dots()
    return result_dict


def format_ellipsized(
    obj: object,
    max_items_to_show: int = 10,
    max_item_length: int = 1024,
) -> str:
    """Pformat ellipsized `obj`.

    Use [pprint.pformat](https://docs.python.org/3/library/pprint.html)
    to convert ellipsize result into string

    Args:
        obj: Python object to ellipsize
        max_items_to_show: if List or Dict in obj (including nested) has more items,
            then show ".." instead of the rest items
        max_item_length: if List's or Dict's item are not another List/Dict
            and its string representation is longer, show ".." instead of the rest of it
    """
    return pformat(
        ellipsize(
            obj,
            max_items_to_show=max_items_to_show,
            max_item_length=max_item_length,
        ),
    )


def print_ellipsized(
    *objs: object,
    max_items_to_show: int = 10,
    max_item_length: int = 1024,
    **kwargs: Any,
) -> None:
    """Print ellipsized `obj` with [pprint](https://docs.python.org/3/library/pprint.html).

    Can print many objects, like general print.
    Pass args to print like [end](https://realpython.com/lessons/sep-end-and-flush/).

    Args:
        objs: Python objects to ellipsize
        max_items_to_show: if List or Dict in objs (including nested) has more items,
            then show ".." instead of the rest items
        max_item_length: if List's or Dict's item are not another List/Dict
            and its string representation is longer, show ".." instead of the rest of it
    """
    print(
        *[
            pformat(
                ellipsize(
                    obj,
                    max_items_to_show=max_items_to_show,
                    max_item_length=max_item_length,
                ),
            )
            for obj in objs
        ],
        **kwargs,
    )
