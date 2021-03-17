"""
qrztools commandline interface
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


import argparse
from getpass import getpass
from dataclasses import asdict
from typing import Dict, Any
from enum import Enum
from sys import stderr

from qrztools import QrzSync, QrzError

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.style import Style
    from rich.pretty import Pretty
    from rich.syntax import Syntax
    from rich.columns import Columns
except ModuleNotFoundError:
    print("To use the qrztools CLI you must install 'rich'", file=stderr)
    raise SystemExit(42)


def tabulate(d: Dict[str, Any], colour: bool = False) -> str:
    result = ""
    for field, val in d.items():
        if isinstance(val, list):
            val = "\n    " + "\n    ".join(val)
        if isinstance(val, Enum):
            val = val.value
        elif isinstance(val, dict):
            if colour:
                val = "\n    " + "\n    ".join([f"[yellow]{k}:[/yellow] {v}" for k, v in val.items()])
            else:
                val = "\n    " + "\n    ".join([f"{k}: {v}" for k, v in val.items()])
        if colour:
            result += f"[blue]{field}:[/blue] [default]{val}[/default]\n"
        else:
            result += f"{field}: {val}\n"
    return result.rstrip("\n")


parser = argparse.ArgumentParser(prog="qrztools",
                                 description=("Retrieve data from QRZ.com, including callsign data, biography content, "
                                              "and DXCC prefix information."))
parser.add_argument("--no-pretty", required=False, action="store_false", dest="pretty",
                    help="Don't pretty-print output")
parser.add_argument("-u", "--user", "--username", required=False, type=str, dest="username", action="store",
                    help="QRZ Username. If not specified, it will be asked for")
parser.add_argument("-p", "--pass", "--password", required=False, type=str, dest="password", action="store",
                    help="QRZ Password. If not specified, it will be asked for")
parser.add_argument("-c", "--call", "--callsign", required=False, type=str, metavar="CALL", dest="call",
                    action="append", help="The callsign to look up")
parser.add_argument("-b", "--bio", "--biography", required=False, type=str, metavar="CALL", dest="bio",
                    action="append", help="The callsign to get biography content for")
parser.add_argument("-d", "--dxcc", required=False, type=str, metavar="NUM|CALL|all", dest="dxcc",
                    action="append", help=("The callsign or DXCC entity number to look up, or 'all' "
                                           "to get all DXCC entities. Warning: 'all' gives a lot of data"))
args = parser.parse_args()

if args.pretty:
    c = Console()
    ec = Console(stderr=True, style="bold red")


if args.username:
    username = args.username
else:
    username = input("QRZ Username: ")

if args.password:
    password = args.password
else:
    password = getpass("QRZ Password: ")


qrz = QrzSync(username=username, password=password)

print()

if args.call:
    for call in args.call:
        try:
            res = qrz.get_callsign(call)
            if args.pretty:
                c.print(
                    Panel.fit(
                        tabulate(asdict(res), True),
                        title=f"Callsign: {call}",
                        border_style=Style(color="green")
                    )
                )
            else:
                print(tabulate(asdict(res)))
        except QrzError as e:
            if args.pretty:
                ec.print(
                    Panel.fit(
                        str(e),
                        title=f"Callsign: {call}",
                        style=Style(color="red"),
                        border_style=Style(color="red")
                    )
                )
            else:
                print(e)
        print()

if args.bio:
    for bio in args.bio:
        try:
            res = qrz.get_bio(bio)
            if args.pretty:
                c.print(
                    Panel.fit(
                        Syntax(res, "html", theme="inkpot", background_color="default"),
                        title=f"Bio: {bio}",
                        border_style=Style(color="green")
                    )
                )
            else:
                print(res)
        except QrzError as e:
            if args.pretty:
                ec.print(
                    Panel.fit(
                        Pretty(e),
                        title=f"Bio: {bio}",
                        border_style=Style(color="red")
                    )
                )
            else:
                print(e)
        print()

if args.dxcc:
    for dxcc in args.dxcc:
        try:
            results = qrz.get_dxcc(dxcc)
            if isinstance(results, list):
                resses = {res.name: tabulate(asdict(res), args.pretty) for res in results}
                if args.pretty:
                    c.print(
                        Panel.fit(
                            Columns(
                                Panel.fit(
                                    r,
                                    title=f"DXCC: {name}",
                                    border_style=Style(color="green")
                                ) for name, r in resses.items()
                            ),
                            title="All DXCC Entities",
                            border_style=Style(color="green")
                        )
                    )
                else:
                    for r in resses.values():
                        print(r)
                        print()
            else:
                res = results
                if args.pretty:
                    c.print(
                        Panel.fit(
                            tabulate(asdict(res), True),
                            title=f"DXCC: {dxcc}",
                            border_style=Style(color="green")
                        )
                    )
                else:
                    print(tabulate(asdict(res)))
        except QrzError as e:
            if args.pretty:
                ec.print(
                    Panel.fit(
                        str(e),
                        title=f"DXCC: {dxcc}",
                        style=Style(color="red"),
                        border_style=Style(color="red")
                    )
                )
            else:
                print(e)
        print()
