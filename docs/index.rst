========
QRZTools
========

.. WARNING:: This library is now deprecated. Use `callsignlookuptools <https://pypi.org/project/callsignlookuptools/>`_ instead.

A QRZ API interface in Python with sync and async support.

.. highlight:: none

.. toctree::
    :hidden:
    :maxdepth: 2

    cli
    api
    types

Installation
============

``qrztools`` requires Python 3.8 at minimum. Install by running:

.. code-block:: sh

    # synchronous requests only
    $ pip install qrztools

    # asynchronous aiohttp only
    $ pip install qrztools[async]

    # both sync and async
    $ pip install qrztools[all]

    # enable the CLI
    $ pip install qrztools[cli]

.. NOTE:: If ``requests``, ``aiohttp``, or ``rich`` are installed another way, you will also have access to the sync, async, or command-line interface, respectively.

License
=======

Copyright 2021 classabbyamp, 0x5c

Released under the BSD 3-Clause License. See ``LICENSE`` for the full license text.
