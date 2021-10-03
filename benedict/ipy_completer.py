# +
#
# This file is reworked from h5py, a low-level Python interface to the HDF5 library.
#
# Originally contributed by Darren Dale
#
# Copyright (C) 2009 Darren Dale
#
# http://h5py.org
# License: BSD  (See LICENSE.txt for full license)
#
# -


import posixpath
import re
import readline
from .dicts import benedict


try:
    # >=ipython-1.0
    from IPython import get_ipython
except ImportError:
    try:
        # support >=ipython-0.11, <ipython-1.0
        from IPython.core.ipapi import get as get_ipython
    except ImportError:
        # support <ipython-0.11
        from IPython.ipapi import get as get_ipython
try:
    # support >=ipython-0.11
    from IPython.utils import generics
except ImportError:
    # support <ipython-0.11
    from IPython import generics

try:
    from IPython.core.error import TryNext
except ImportError:
    try:
        from IPython import TryNext
    except ImportError:
        from IPython.ipapi import TryNext


re_item_match = re.compile(r"""(?:.*\=)?(.*)\[(?P<s>['|"])(?!.*(?P=s))(.*)$""")


def completer(self, event):
    """ Completer function to be loaded into IPython """
    try:
        base, item = re_item_match.split(event.line)[1:4:2]
    except ValueError:
        return []

    # `base` should now contain all chars in the current line up to the
    # benedict instance where tab completeion was invoked
    # we also want to be able to complete when passing a benedict as an
    # argument to a function. then a "(" will be in `base`
    if "(" in base:
        try:
            base = base.split("(")[-1]
            if not isinstance(self._ofind(base).get("obj"), benedict):
                raise ValueError
        except Exception as e:
            return []

    # if completing a benedict, get the separator to split paths, else skip completion
    if isinstance(self._ofind(base).get("obj"), benedict):
        try:
            # older versions of IPython:
            obj = eval(base, self.shell.user_ns)
        except AttributeError:
            # as of IPython-1.0:
            obj = eval(base, self.user_ns)
        sep = obj.keypath_separator
    else:
        raise TryNext

    # per default, posixpath uses '/' as a sperator
    # path, _ = posixpath.split(item)
    # we want: empty string when no sep, else everything before the last sep.
    path = ""
    if len(item) >= 1 and item[0] == sep:
        # this is not great, keys without a name are problematic
        return []
    elif len(item) > 1:
        if item[-1] == sep:
            path = item[:-1]
        else:
            path = sep.join(item.split(sep)[:-1])

    # maybe it is convenient to close the brackets.
    # ideally this would not be shown in the preview, but no clue how to do this
    term = ""
    if re.search('\["', event.line):
        term = '"]'
    elif re.search("\['", event.line):
        term = "']"

    try:
        if len(path) > 0:
            items = (sep.join([path, name]) for name in obj[path].keys())
        else:
            items = obj.keys()
    except AttributeError:
        return []

    items = [
        item + sep if isinstance(obj[item], benedict) else item + term for item in items
    ]
    items = list(items)
    readline.set_completer_delims(" \t\n`!@#$^&*()=+[{]}\\|;:'\",<>?")

    return [i for i in items if i[: len(item)] == item]


def load_ipython_extension(ip=None):
    """ Load completer function into IPython """
    if ip is None:
        ip = get_ipython()
    ip.set_hook("complete_command", completer, re_key=r"(?:.*\=)?(.+?)\[")
