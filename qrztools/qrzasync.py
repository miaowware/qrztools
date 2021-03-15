"""
qrztools: asynchronous editon
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


from typing import Dict, Union, Optional
from io import BytesIO

from lxml import etree
import aiohttp

from .__info__ import __version__
from .qrztools import QrzAbc, QrzCallsignData, QrzDxccData, QrzError, BASE_URL


class QrzAsync(QrzAbc):
    """The asynchronous QRZ API object

    :param username: QRZ username
    :type username: str
    :param password: QRZ password
    :type password: str
    :param session_key: QRZ login session key
    :type session_key: str
    :param useragent: Useragent for QRZ
    :type useragent: str
    :param session: An aiohttp session to use for requests
    :type session: Optional[aiohttp.ClientSession]
    """
    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = f"python-qrztools-v{__version__}",
                 session: Optional[aiohttp.ClientSession] = None):
        self._session = session
        super().__init__(username, password, session_key=session_key, useragent=useragent)

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        :getter: gets the aiohttp session
        :rtype: aiohttp.ClientSession

        :setter: sets the aiohttp session
        :type: aiohttp.ClientSession
        """
        return self._session

    @session.setter
    def session(self, val: aiohttp.ClientSession) -> None:
        self._session = val

    async def start_session(self) -> None:
        self._session = aiohttp.ClientSession()

    async def close_session(self) -> None:
        await self._session.close()

    async def get_callsign(self, callsign: str) -> QrzCallsignData:
        try:
            await self._check_session()
        except QrzError:
            await self._login()
        resp_xml = await self._do_query({"s": self._session_key, "callsign": callsign.upper()})
        if isinstance(resp_xml, etree._Element):
            return self._process_callsign(resp_xml)
        return QrzCallsignData("Unknown")

    async def get_bio(self, callsign: str) -> str:
        try:
            await self._check_session()
        except QrzError:
            await self._login()
        bio = await self._do_query({"s": self._session_key, "html": callsign.upper()})
        if isinstance(bio, str):
            return bio
        return ""

    async def get_dxcc(self, query: Union[str, int]) -> QrzDxccData:
        if isinstance(query, int):
            query = str(query)
        if query.lower() == "all":
            raise NotImplementedError("Getting all DXCC data is not supported at this time.")
        try:
            await self._check_session()
        except QrzError:
            await self._login()
        resp_xml = await self._do_query({"s": self._session_key, "dxcc": query.upper()})
        if isinstance(resp_xml, etree._Element):
            return self._process_dxcc(resp_xml)
        return QrzDxccData()

    async def _login(self) -> None:
        resp_xml = await self._do_query(
                {"username": self._username, "password": self._password, "agent": self._useragent}
            )
        if isinstance(resp_xml, etree._Element):
            self._process_login(resp_xml)

    async def _check_session(self) -> None:
        resp_xml = await self._do_query({"s": self._session_key})
        if isinstance(resp_xml, etree._Element):
            self._process_check_session(resp_xml)

    async def _do_query(self, query: Dict[str, str]) -> Union[str, etree._Element]:
        url = BASE_URL + ";".join(f"{k}={v}" for k, v in query.items())
        async with self._session.get(url) as resp:
            if resp.status != 200:
                raise QrzError(f"Unable to connect to QRZ (HTTP Error {resp.status})")
            if "html" in query:
                return str(await resp.text())
            with BytesIO(await resp.read()) as resp_file:
                return etree.parse(resp_file).getroot()
