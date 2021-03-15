"""
qrztools: synchronous editon
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Dict, Union
from io import BytesIO

from lxml import etree
import requests

from .__info__ import __version__
from .qrztools import QrzAbc, QrzCallsignData, QrzDxccData, QrzError, BASE_URL


class QrzSync(QrzAbc):
    """The synchronous QRZ API object

    :param username: QRZ username
    :type username: str
    :param password: QRZ password
    :type password: str
    :param session_key: QRZ login session key
    :type session_key: str
    :param useragent: Useragent for QRZ
    :type useragent: str
    :param session: A requests session to use for requests
    :type session: requests.Session
    """
    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = f"python-qrztools-v{__version__}", session: requests.Session = requests.Session()):
        self._session = session
        super().__init__(username, password, session_key=session_key, useragent=useragent)

    @property
    def session(self) -> requests.Session:
        """
        :getter: gets the requests session
        :rtype: requests.Session

        :setter: sets the requests session
        :type: requests.Session
        """
        return self._session

    @session.setter
    def session(self, val: requests.Session) -> None:
        self._session = val

    def get_callsign(self, callsign: str) -> QrzCallsignData:
        try:
            self._check_session()
        except QrzError:
            self._login()
        resp_xml = self._do_query({"s": self._session_key, "callsign": callsign.upper()})
        if isinstance(resp_xml, etree._Element):
            return self._process_callsign(resp_xml)
        return QrzCallsignData("Unknown")

    def get_bio(self, callsign: str) -> str:
        try:
            self._check_session()
        except QrzError:
            self._login()
        bio = self._do_query({"s": self._session_key, "html": callsign.upper()})
        if isinstance(bio, str):
            return bio
        return ""

    def get_dxcc(self, query: Union[str, int]) -> QrzDxccData:
        if isinstance(query, int):
            query = str(query)
        if query.lower() == "all":
            raise NotImplementedError("Getting all DXCC data is not supported at this time.")
        try:
            self._check_session()
        except QrzError:
            self._login()
        resp_xml = self._do_query({"s": self._session_key, "dxcc": query.upper()})
        if isinstance(resp_xml, etree._Element):
            return self._process_dxcc(resp_xml)
        return QrzDxccData()

    def _login(self) -> None:
        resp_xml = self._do_query({"username": self._username, "password": self._password, "agent": self._useragent})
        if isinstance(resp_xml, etree._Element):
            self._process_login(resp_xml)

    def _check_session(self) -> None:
        resp_xml = self._do_query({"s": self._session_key})
        if isinstance(resp_xml, etree._Element):
            self._process_check_session(resp_xml)

    def _do_query(self, query: Dict[str, str]) -> Union[str, etree._Element]:
        url = BASE_URL + ";".join(f"{k}={v}" for k, v in query.items())
        with self._session.get(url) as resp:
            if resp.status_code != 200:
                raise QrzError(f"Unable to connect to QRZ (HTTP Error {resp.status_code})")
            if "html" in query:
                return resp.text
            with BytesIO(resp.content) as resp_bytes:
                return etree.parse(resp_bytes).getroot()
