=========
CLI Usage
=========

.. highlight:: none

.. NOTE:: To use the CLI, install with the extra ``cli`` (e.g. ``pip install qrztools[cli]``) or otherwise install the library ``rich``.

``qrztools`` has a basic CLI interface, which can be run using:

.. code-block:: sh

    $ python3 -m qrztools

It can be used with the following arguments::

    usage: qrztools [-h] [--no-pretty] [-u USERNAME] [-p PASSWORD] [-c CALL] [-b CALL] [-d NUM|CALL|all]

    Retrieve data from QRZ.com, including callsign data, biography content, and DXCC prefix information.

    optional arguments:
      -h, --help            show this help message and exit
      --no-pretty           Don't pretty-print output
      -u USERNAME, --user USERNAME, --username USERNAME
                            QRZ Username. If not specified, it will be asked for
      -p PASSWORD, --pass PASSWORD, --password PASSWORD
                            QRZ Password. If not specified, it will be asked for
      -c CALL, --call CALL, --callsign CALL
                            The callsign to look up
      -b CALL, --bio CALL, --biography CALL
                            The callsign to get biography content for
      -d NUM|CALL|all, --dxcc NUM|CALL|all
                            The callsign or DXCC entity number to look up, or 'all' to get all DXCC entities. Warning: 'all' gives a lot of data
