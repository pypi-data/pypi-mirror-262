# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Iterable

try:
    from django.http.response import HttpResponseBase

    django_response_types = (HttpResponseBase,)
except ImportError:  # pragma: no cover
    django_response_types = ()

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

string_types = (str, bytes, bytearray)

list_iterator = type(iter(list()))
dict_iterator = type(iter(dict()))


def is_iterable(value):
    """
    :param value: any type
    :return: True if iterable type like list, dict but NOT string
             False if string or any other type like database collection types
                   (pymongo Collection implements iter but is not an iterable

    An iterable should meet one of the following conditions:
        * Has both __next__ and __iter__ methods, or
        * Has __getitem__ method

    For the purposes of Assess, we want to exclude stringy types from iteration.

    See https://stackoverflow.com/a/61139278 and associated question for
    relevant discussion.
    """
    return not isinstance(value, string_types) and (
        hasattr(value, "__getitem__") or isinstance(value, Iterable)
    )


def len_or_zero(value):
    try:
        return len(value)
    except Exception:
        return 0


def safe_iterator(it):
    if isinstance(it, (list_iterator, dict_iterator)):
        logger.debug(
            "WARNING: skipping iteration of non-seekable iterator: %s", type(it)
        )
        return

    if isinstance(it, (str, list, dict, tuple)) or (
        isinstance(it, django_response_types)
        and not safe_getattr(it, "streaming", True)
    ):
        yield from it
        return

    if not (hasattr(it, "tell") and hasattr(it, "seek")):
        logger.debug("WARNING: skipping iteration of non-seekable object: %s", type(it))
        return

    try:
        orig_pos = it.tell()
    except Exception:
        logger.debug(
            "WARNING: skipping iteration of non-tell()-able object: %s", type(it)
        )
        return

    try:
        yield from it
    except Exception:
        logger.debug("safe_iterator failed to iterate over %s", type(it))
    finally:
        it.seek(orig_pos)


def safe_getattr(obj, attr, default=None):
    """
    A getattr implementation that returns a default even if an exception is raised

    Some classes may override __getattribute__ to raise exceptions when certain
    attributes are accessed. When we are dealing with objects from the outside world,
    we want to be careful in our attribute access to avoid such exceptions and provide
    a safe default.
    """
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default


def safe_getattr_list(obj, attr_names, default):
    """
    Try getattr for a list of several attribute names, returning the first one found. If
    none of the provided attributes exist on the object, return the default instead.
    """

    class NoAttr:
        pass

    for attr_name in attr_names:
        value = safe_getattr(obj, attr_name, NoAttr)
        if value is not NoAttr:
            return value
    return default
