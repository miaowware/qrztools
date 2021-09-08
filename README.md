# qrztools

# **WARNING:** This library is now deprecated. Use [callsignlookuptools](https://pypi.org/project/callsignlookuptools/) instead.

QRZ API interface in Python

[![PyPI](https://img.shields.io/pypi/v/qrztools)](https://pypi.org/project/qrztools/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qrztools) ![PyPI - License](https://img.shields.io/pypi/l/qrztools) [![Documentation Status](https://readthedocs.org/projects/qrztools/badge/?version=latest)](https://qrztools.readthedocs.io/en/latest/?badge=latest)

## Installation

`qrztools` requires Python 3.8 at minimum.

```sh
# synchronous requests only
$ pip install qrztools

# asynchronous aiohttp only
$ pip install qrztools[async]

# both sync and async
$ pip install qrztools[all]

# enable the CLI
$ pip install qrztools[cli]
```

**Note:** If `requests`, `aiohttp`, or `rich` are installed another way, you will also have access to the sync, async, or command-line interface, respectively.

## Documentation

Documentation is available on [ReadTheDocs](https://qrztools.miaow.io/).

## Copyright

Copyright 2021 classabbyamp, 0x5c  
Released under the BSD 3-Clause License.  
See [`LICENSE`](LICENSE) for the full license text.
