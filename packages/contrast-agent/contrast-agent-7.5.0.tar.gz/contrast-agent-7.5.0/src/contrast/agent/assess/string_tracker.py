# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from typing import Any

import sys
from collections import OrderedDict
import time
from weakref import WeakValueDictionary

from contrast.agent import scope
from contrast.assess_extensions import cs_str
from contrast.utils.decorators import fail_quietly
from contrast.utils.string_utils import truncated_signature

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class _NoDefault:
    # unique value used for `pop()` override
    pass


class StringTracker(OrderedDict):
    AGE_OFF_THRESHOLD_SECS = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pointer_to_props_map = WeakValueDictionary()

    def track(self, value):
        if not isinstance(value, (str, bytes, bytearray)):
            return None

        # ignore probable interned strings
        # TODO: PYT-2365 use is_interned here
        if len(value) < 2:
            return None

        if value and value not in self:
            from contrast.agent.assess.properties import Properties

            props = Properties(value)
            self.log_tracked(value)
            self[value] = props

        return self[value]

    def update_pointer_map(self, value, props):
        """
        Update mapping between str objects and their underlying char buffers

        We need to maintain this mapping in order to implement the hook for the
        exec statement in PY2. This is because the function we hook does not
        actually get a PyObject * as an argument, but only a char *. Since
        there is a 1-to-1 correspondence between the char * and the PyObject *,
        we can do a reverse lookup based on the pointer value in order to
        detect tracked strings that get passed to the exec statement.
        """
        ptr_val = cs_str.get_str_pointer(value)
        if ptr_val is None:
            return

        self.pointer_to_props_map[ptr_val] = props

    def lookup_by_pointer(self, ptr_val):
        return self.pointer_to_props_map.get(ptr_val)

    def log_tracked(self, value):
        self._truncate_and_log("tracking new string", value)

    def log_ageoff(self, value):
        self._truncate_and_log("aging off string from tracker", value)

    def _truncate_and_log(self, msg, value):
        with scope.contrast_scope():
            logger.debug("%s: %s", msg, truncated_signature(value))

    def update_properties(self, value, properties):
        self[value] = properties

    def __delitem__(self, key):
        return super().__delitem__(id(key))

    def __getitem__(self, key):
        return super().__getitem__(id(key))

    def __setitem__(self, key, value):
        if key in self:
            return super(OrderedDict, self).__setitem__(id(key), value)
        return super().__setitem__(id(key), value)

    def get(self, key, default=None):
        return super().get(id(key), default)

    if sys.version_info[:2] >= (3, 11):
        # Prior to 3.11, `pop` likely uses `__getitem__` under the hood. However, this
        # is no longer true in 3.11, which means we need to override this method.
        def pop(self, key, default: Any = _NoDefault):
            if default is _NoDefault:
                return super().pop(id(key))
            return super().pop(id(key), default)

    def __contains__(self, key):
        return super().__contains__(id(key))

    def get_by_id(self, key_id):
        return super().__getitem__(key_id)

    @fail_quietly("Failure in string tracker ageoff")
    @scope.with_contrast_scope
    def ageoff(self):
        """
        Age-off string tracker entries older than predefined threshold.

        NOTE: It is only approximately true that this OrderedDict's values are sorted by
        timestamp. They are in insertion-order, but timestamps can change due to
        circumstances that are currently not well-understood. Do not assume timestamps
        are in order.

        TODO: PYT-2365 - we believe incorrect string tracker timestamps may be affected
        by string interning. When this ticket is completed, check to make sure ageoff
        is still working as expected.
        """
        now = time.time()
        logger.debug("String tracker length (pre-ageoff): %s", len(self))
        # Keys are IDs in this loop
        for key in list(self.keys()):
            props = super().get(key)
            if (
                props is not None
                and (now - props.timestamp) > self.AGE_OFF_THRESHOLD_SECS
            ):
                self.log_ageoff(props.origin)
                try:
                    super().__delitem__(key)
                except KeyError:
                    # Handles potential race condition that may occur if
                    # another thread may have already deleted the key after
                    # this thread gets the key but before it deletes it.
                    # More likely to happen in multi-threaded apps and if
                    # and app receives many requests per second.
                    pass
