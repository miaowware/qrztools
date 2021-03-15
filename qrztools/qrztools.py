"""
qrztools
---
Copyright 2021 classabbyamp, 0x5c
Released under the terms of the BSD 3-Clause license.
"""


import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
from datetime import datetime

from gridtools import LatLong, Grid
from lxml import etree

from .__info__ import __version__


BASE_URL = "https://xmldata.qrz.com/xml/current/?"


class QrzError(Exception):
    """The exception raised when something goes wrong in qrztools"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


@dataclass
class QrzImage:
    """Represents a QRZ profile image"""
    #: image url
    url: str = ""
    #: image height in pixels
    height: int = 0
    #: image width in pixels
    width: int = 0
    #: approximate size in bytes
    size: int = 0


@dataclass
class Dxcc:
    """Represents a DXCC entity in a :class:`QrzCallsignData` object"""
    #: entity ID
    id: int = 0
    #: entity name
    name: str = ""


@dataclass
class Address:
    """Represents an address in a :class:`QrzCallsignData` object"""
    #: Attention address line, this line should be prepended to the address
    attn: str = ""
    #: address line 1 (i.e. house # and street)
    line1: str = ""
    #: address line 2 (i.e, city name)
    line2: str = ""
    #: state (USA Only)
    state: str = ""
    #: Zip/postal code
    zip: str = ""
    #: country name for the QSL mailing address
    country: str = ""
    #: dxcc entity code for the mailing address country
    ccode: int = 0


@dataclass
class Name:
    """Represents a name in a :class:`QrzCallsignData` object"""
    #: first name(s)
    first: str = ""
    #: last name or full name
    name: str = ""
    #: A different or shortened name used on the air
    nickname: str = ""
    #: Combined full name and nickname in the format used by QRZ. This fortmat is subject to change.
    formatted_name: str = ""


class GeoLocSource(enum.Enum):
    """Describes where the lat/long data in a :class:`QrzCallsignData` object comes from"""
    USER = "User"
    GEOCODE = "Geocode"
    GRID = "Grid"
    ZIP = "Zip Code"
    STATE = "State"
    DXCC = "DXCC"
    NONE = "None"


class Continent(enum.Enum):
    """A continent, used for :class:`QrzDxccData`"""
    AF = "Africa"
    AN = "Antarctica"
    AS = "Asia"
    EU = "Europe"
    NA = "North America"
    OC = "Oceania"
    SA = "South America"


@dataclass
class QrzCallsignData:
    """A QRZ callsign query result."""
    # callsign-related things
    #: Callsign
    call: str
    #: Cross reference: the query callsign that returned this record
    xref: str = ""
    #: Other callsigns that resolve to this record
    aliases: List[str] = field(default_factory=list)
    #: Previous callsign
    prev_call: str = ""
    #: QSL manager info
    qsl_manager: str = ""
    #: license effective date (USA)
    effective_date: datetime = datetime.min
    #: license expiration date (USA)
    expire_date: datetime = datetime.min
    #: license class
    lic_class: str = ""
    #: license type codes (USA)
    lic_codes: str = ""

    #: Operator name
    name: Name = Name()
    # location-related things
    #: Operator mailing address
    address: Address = Address()
    #: DXCC entity
    dxcc: Dxcc = Dxcc()
    #: approximate lat/long of address
    latlong: LatLong = LatLong(0, 0)
    #: grid locator of address
    grid: Grid = Grid(LatLong(0, 0))
    #: county name (USA)
    county: str = ""
    #: FIPS county identifier (USA)
    fips: str = ""
    #: Metro Service Area (USPS)
    msa: str = ""
    #: Telephone Area Code (USA)
    area_code: str = ""
    #: CQ zone identifier
    cq_zone: int = 0
    #: ITU zone identifier
    itu_zone: int = 0
    #: birthdate of the operator
    born: datetime = datetime.min
    #: IOTA designator
    iota: str = ""
    #: Describes source of lat/long data
    geoloc: GeoLocSource = GeoLocSource.NONE

    # time-related things
    #: Time zone name (USA)
    timezone: str = ""
    #: GMT time offset
    gmt_offset: str = ""
    #: whether daylight savings time is observed
    observes_dst: bool = False

    # profile-related things
    #: User who manages this callsign on QRZ
    user: str = ""
    #: email address
    email: str = ""
    #: profile url
    url: str = ""
    #: QRZ web page views
    profile_views: int = 0
    #: approximate size of bio HTML in bytes
    bio_size: int = 0
    #: date of last bio update
    bio_updated: datetime = datetime.min
    #: QRZ profile image
    image: QrzImage = QrzImage()
    #: QRZ database serial number
    serial: int = 0
    #: QRZ callsign last modified date
    last_modified: datetime = datetime.min
    #: whether the operator accepts eQSL
    eqsl: bool = False
    #: whether the operator accepts mail QSL
    mail_qsl: bool = False
    #: whether the operator accepts Logbook of the World QSL
    lotw_qsl: bool = False


@dataclass
class QrzDxccData:
    """A QRZ DXCC query result."""
    #: entity number
    dxcc: int = 0
    #: ISO-3166-1 alpha-2 country code
    cc2: str = ""
    #: ISO-3166-1 alpha-3 country code
    cc3: str = ""
    #: entity name
    name: str = ""
    #: the entity's continent
    continent: Optional[Continent] = None
    #: the entity's ITU zone
    ituzone: int = 0
    #: the entity's CQ zone
    cqzone: int = 0
    #: UTC timezone offset. Odd timezones, such as 0545 mean "5 hours, 45 minutes".
    utc_offset: str = ""
    #: approximate latitude and longitude of the entity
    latlong: LatLong = LatLong(0, 0)
    #: special notes/exceptions
    notes: str = ""


class QrzAbc(ABC):
    """The base class for QrzSync and QrzAsync. **This should not be used directly.**"""
    def __init__(self, username: str, password: str, session_key: str = "",
                 useragent: str = f"python-qrztools-v{__version__}"):
        self._username = username
        self._password = password
        self._useragent = useragent
        self._session_key = session_key

    @property
    def username(self) -> str:
        """
        :getter: gets QRZ username
        :rtype: str

        :setter: sets QRZ username
        :type: str
        """
        return self._username

    @username.setter
    def username(self, val: str) -> None:
        self._username = val

    @property
    def password(self) -> str:
        """
        :getter: gets QRZ password
        :rtype: str

        :setter: sets QRZ password
        :type: str
        """
        return self._password

    @password.setter
    def password(self, val: str) -> None:
        self._password = val

    @property
    def useragent(self) -> str:
        """
        :getter: gets QRZ useragent
        :rtype: str

        :setter: sets QRZ useragent
        :type: str
        """
        return self._useragent

    @useragent.setter
    def useragent(self, val: str) -> None:
        self._useragent = val

    @property
    @abstractmethod
    def session(self):
        return self._session

    @session.setter
    @abstractmethod
    def session(self, val) -> None:
        self._session = val

    @property
    def session_key(self) -> str:
        """
        :getter: gets QRZ session key
        :rtype: str

        :setter: sets QRZ session key
        :type: str
        """
        return self._session_key

    @session_key.setter
    def session_key(self, val: str) -> None:
        self._session_key = val

    @abstractmethod
    def get_callsign(self, callsign: str) -> QrzCallsignData:
        """Gets QRZ data for a callsign.

        :param callsign: the callsign to search for
        :type callsign: str
        :return: the QRZ data for the callsign
        :rtype: QrzCallsignData
        """
        pass

    @abstractmethod
    def get_bio(self, callsign: str) -> str:
        """Get the HTML for the bio of a callsign

        :param callsign: the callsign to search for
        :type callsign: str
        :return: the bio HTML
        :rtype: str
        """
        pass

    @abstractmethod
    def get_dxcc(self, query: Union[str, int]) -> QrzDxccData:
        """Get data about a DXCC entity from a DXCC entity number or callsign.

        :param query: a DXCC entity number or callsign
        :type query: Union[str, int]
        :return: the data about the DXCC entity
        :rtype: QrzDxccData
        """
        pass

    @abstractmethod
    def _login(self) -> None:
        pass

    @abstractmethod
    def _check_session(self) -> None:
        pass

    @abstractmethod
    def _do_query(self, query: Dict[str, str]) -> Union[str, etree._Element]:
        pass

    def _process_callsign(self, resp_xml: etree._Element) -> QrzCallsignData:
        # check for errors like "not found"
        self._process_check_session(resp_xml)
        resp_xml_data = resp_xml.xpath("/x:QRZDatabase/x:Callsign", namespaces={"x": "http://xmldata.qrz.com"})
        data = {el.tag.split("}")[1]: el.text for el in resp_xml_data[0].getiterator()}  # type: ignore

        calldata = QrzCallsignData(call=data.get("call", "").upper())

        calldata.xref = data.get("xref", "").upper()

        aliases = data.get("aliases", [])
        calldata.aliases = aliases.upper().split(",") if aliases else aliases

        calldata.prev_call = data.get("p_call", "").upper()
        calldata.qsl_manager = data.get("qslmgr", "")

        efdate = data.get("efdate", datetime.min)
        calldata.effective_date = datetime.strptime(efdate, "%Y-%m-%d") if not isinstance(efdate, datetime) else efdate

        expdate = data.get("expdate", datetime.min)
        calldata.expire_date = datetime.strptime(expdate, "%Y-%m-%d") if not isinstance(expdate, datetime) else expdate

        calldata.lic_class = data.get("class", "")
        calldata.lic_codes = data.get("codes", "")

        calldata.name = Name(
            first=data.get("fname", ""),
            name=data.get("name", ""),
            nickname=data.get("nickname", ""),
            formatted_name=data.get("name_fmt", "")
        )

        calldata.address = Address(
            attn=data.get("attn", ""),
            line1=data.get("addr1", ""),
            line2=data.get("addr2", ""),
            state=data.get("state", ""),
            zip=data.get("zip", ""),
            country=data.get("country", ""),
            ccode=int(data.get("ccode", 0))
        )

        calldata.dxcc = Dxcc(int(data.get("dxcc", 0)), data.get("land", ""))
        calldata.latlong = LatLong(float(data.get("lat", 0)), float(data.get("lon", 0)))
        calldata.grid = Grid(data.get("grid", LatLong(0, 0)))
        calldata.county = data.get("county", "")
        calldata.fips = data.get("fips", "")
        calldata.msa = data.get("MSA", "")
        calldata.area_code = data.get("AreaCode", "")
        calldata.cq_zone = int(data.get("cqzone", 0))
        calldata.itu_zone = int(data.get("ituzone", 0))

        born = data.get("born", datetime.min)
        calldata.born = datetime.strptime(born, "%Y-%m-%d") if not isinstance(born, datetime) else born
        calldata.iota = data.get("iota", "")

        geoloc = data.get("geoloc", None).lower()
        if geoloc == "user":
            calldata.geoloc = GeoLocSource.USER
        elif geoloc == "geocode":
            calldata.geoloc = GeoLocSource.GEOCODE
        elif geoloc == "grid":
            calldata.geoloc = GeoLocSource.GRID
        elif geoloc == "zip":
            calldata.geoloc = GeoLocSource.ZIP
        elif geoloc == "state":
            calldata.geoloc = GeoLocSource.STATE
        elif geoloc == "dxcc":
            calldata.geoloc = GeoLocSource.DXCC

        calldata.timezone = data.get("TimeZone", "")
        calldata.gmt_offset = data.get("GMTOffset", "")

        dst = data.get("DST", False)
        calldata.observes_dst = True if dst == "1" else False

        calldata.user = data.get("user", "")
        calldata.email = data.get("email", "")
        calldata.url = data.get("url", f"https://www.qrz.com/db/{calldata.call}")
        calldata.profile_views = int(data.get("u_views", 0))
        calldata.bio_size = int(data.get("bio", 0))

        biodate = data.get("biodate", datetime.min)
        if not isinstance(biodate, datetime):
            calldata.bio_updated = datetime.strptime(biodate, "%Y-%m-%d %H:%M:%S")

        img_info = data.get("imageinfo", "0:0:0")
        img_height, img_width, img_size = [int(x) for x in img_info.split(":")]
        calldata.image = QrzImage(
            url=data.get("image", ""),
            height=img_height,
            width=img_width,
            size=img_size
        )

        calldata.serial = data.get("serial", 0)

        last_mod = data.get("moddate", datetime.min)
        if not isinstance(last_mod, datetime):
            calldata.last_modified = datetime.strptime(last_mod, "%Y-%m-%d %H:%M:%S")

        eqsl = data.get("eqsl", "")
        calldata.eqsl = True if eqsl == "1" else False

        mail_qsl = data.get("mqsl", "")
        calldata.mail_qsl = True if mail_qsl == "1" else False

        lotw_qsl = data.get("lotw", "")
        calldata.lotw_qsl = True if lotw_qsl == "1" else False

        return calldata

    def _process_dxcc(self, resp_xml: etree._Element) -> QrzDxccData:
        # check for errors like "not found"
        self._process_check_session(resp_xml)
        resp_xml_data = resp_xml.xpath("/x:QRZDatabase/x:DXCC", namespaces={"x": "http://xmldata.qrz.com"})
        data = {el.tag.split("}")[1]: el.text for el in resp_xml_data[0].getiterator()}  # type: ignore

        dxccdata = QrzDxccData()

        dxccdata.dxcc = int(data.get("dxcc", 0))
        dxccdata.cc2 = data.get("cc", "")
        dxccdata.cc3 = data.get("ccc", "")
        dxccdata.name = data.get("name", "")

        cont = data.get("continent", None)
        if cont == "AF":
            dxccdata.continent = Continent.AF
        elif cont == "AS":
            dxccdata.continent = Continent.AS
        elif cont == "EU":
            dxccdata.continent = Continent.EU
        elif cont == "NA":
            dxccdata.continent = Continent.NA
        elif cont == "OC":
            dxccdata.continent = Continent.OC
        elif cont == "SA":
            dxccdata.continent = Continent.SA

        dxccdata.ituzone = int(data.get("ituzone", 0))
        dxccdata.cqzone = int(data.get("cqzone", 0))
        dxccdata.utc_offset = data.get("timezone", "")
        dxccdata.latlong = LatLong(float(data.get("lat", 0)), float(data.get("lon", 0)))
        dxccdata.notes = data.get("notes", "")

        return dxccdata

    def _process_login(self, resp_xml: etree._Element):
        resp_xml_session = resp_xml.xpath("/x:QRZDatabase/x:Session", namespaces={"x": "http://xmldata.qrz.com"})
        resp_session = {el.tag.split("}")[1]: el.text for el in resp_xml_session[0].getiterator()}  # type: ignore
        if "Error" in resp_session:
            raise QrzError(resp_session["Error"])
        if resp_session["SubExp"] == "non-subscriber":
            raise QrzError("Invalid QRZ Subscription")
        self._session_key = resp_session["Key"]

    def _process_check_session(self, resp_xml: etree._Element):
        resp_xml_session = resp_xml.xpath("/x:QRZDatabase/x:Session", namespaces={"x": "http://xmldata.qrz.com"})
        resp_session = {el.tag.split("}")[1]: el.text for el in resp_xml_session[0].getiterator()}  # type: ignore
        if "Error" in resp_session:
            raise QrzError(resp_session["Error"])
