=====
Types
=====

.. WARNING:: This library is now deprecated. Use `callsignlookuptools <https://pypi.org/project/callsignlookuptools/>`_ instead.

.. highlight:: none

.. module:: qrztools.qrztools

Callsign Data
=============

.. autoclass:: QrzCallsignData()
    :exclude-members: effective_date, expire_date, name, address, dxcc, latlong, grid, born, bio_updated, image, last_modified

    .. autoattribute:: name
        :annotation: : Name = Name()

    .. autoattribute:: address
        :annotation: : Address = Address()

    .. autoattribute:: dxcc
        :annotation: : Dxcc = Dxcc()

    .. autoattribute:: latlong
        :annotation: : LatLong = LatLong(0, 0)

    .. autoattribute:: grid
        :annotation: : Grid = Grid(LatLong(0, 0))

    .. autoattribute:: image
        :annotation: : QrzImage = QrzImage()

    .. autoattribute:: effective_date
        :annotation: : datetime.datetime = datetime.datetime.min

    .. autoattribute:: expire_date
        :annotation: : datetime.datetime = datetime.datetime.min

    .. autoattribute:: last_modified
        :annotation: : datetime.datetime = datetime.datetime.min

    .. autoattribute:: bio_updated
        :annotation: : datetime.datetime = datetime.datetime.min

    .. autoattribute:: born
        :annotation: : datetime.datetime = datetime.datetime.min

DXCC Data
=========

.. autoclass:: QrzDxccData()
    :exclude-members: latlong

    .. autoattribute:: latlong
        :annotation: : LatLong = LatLong(0, 0)

Helper Data Types
=================

.. autoclass:: QrzImage()

.. autoclass:: Dxcc()

.. autoclass:: Address()

.. autoclass:: Name()

.. autoclass:: GeoLocSource()

.. autoclass:: Continent()

Exceptions
==========

.. autoclass:: QrzError
