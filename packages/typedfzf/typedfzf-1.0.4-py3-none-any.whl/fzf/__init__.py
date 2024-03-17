from __future__ import annotations

try:
    from fzf._version import (  # type: ignore[no-redef,unused-ignore]
        __version__,  #
    )
except ModuleNotFoundError:
    try:
        from setuptools_scm import get_version

        __version__ = get_version(root="..", relative_to=__file__)
    except (ImportError, LookupError):
        msg = "typedfzf is not correctly installed. Please install it with pip."
        raise RuntimeError(msg) from None

from fzf._fzf import *  # noqa: F403
