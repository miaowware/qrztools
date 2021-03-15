"""
qrztools
---
QRZ API interface in Python

Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""

from importlib.util import find_spec

from .__info__ import __version__  # noqa: F401

from .qrztools import QrzError, QrzCallsignData, QrzDxccData, QrzAbc  # noqa: F401

if find_spec("requests"):
    from .qrzsync import QrzSync  # noqa: F401
if find_spec("aiohttp"):
    from .qrzasync import QrzAsync  # noqa: F401
if not find_spec("requests") and not find_spec("aiohttp"):
    raise ModuleNotFoundError("At least one of requests or aiohttp needs to be installed to use qrztools")
