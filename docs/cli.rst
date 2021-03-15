=========
CLI Usage
=========

.. highlight:: none

``qrztools`` has a basic CLI interface, which can be run using:

.. code-block:: sh

    $ python3 -m qrztools

It can be used with the following arguments::

    usage: qrztools [-h] [--no-pretty] [-u USERNAME] [-p PASSWORD] [-c CALL] [-b CALL] [-d NUM|CALL]

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
      -d NUM|CALL, --dxcc NUM|CALL
                            The callsign or DXCC entity number to look up
