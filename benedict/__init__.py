# -*- coding: utf-8 -*-

from benedict.dicts import benedict
from benedict.metadata import (
    __author__, __copyright__, __description__,
    __license__, __title__, __version__,
)

def enable_ipython_completer():
    """ Call this from an interactive IPython session to enable tab-completion
    of group and attribute names.
    """
    import sys
    if 'IPython' in sys.modules:
        ip_running = False
        try:
            from IPython.core.interactiveshell import InteractiveShell
            ip_running = InteractiveShell.initialized()
        except ImportError:
            # support <ipython-0.11
            from IPython import ipapi as _ipapi
            ip_running = _ipapi.get() is not None
        except Exception:
            pass
        if ip_running:
            from . import ipy_completer
            return ipy_completer.load_ipython_extension()

    raise RuntimeError('Completer must be enabled in active ipython session')

try:
    enable_ipython_completer()
except Exception as e:
    pass
