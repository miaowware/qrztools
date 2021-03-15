=============
API Reference
=============

.. highlight:: none

``qrztools`` allows for both synchronous and asynchronous usage via two main classes, :class:`qrztools.QrzSync` and :class:`qrztools.QrzAsync`.
These inherit from :class:`qrztools.QrzAbc`. See there for some properties.

.. module:: qrztools

.. autoclass:: QrzAbc
    :exclude-members: get_callsign, get_bio, get_dxcc

Synchronous
===========

.. autoclass:: QrzSync

Asynchronous
============

.. autoclass:: QrzAsync
