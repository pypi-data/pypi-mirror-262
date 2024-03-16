import logging
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, Extra, Field
from pydantic.functional_validators import PlainValidator
from typing_extensions import Annotated, TypeAliasType

from nagra_panorama_api.utils import el2dict


def first(iterable, default=None):
    return next(iter(iterable), default)


DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


def parse_datetime(d):
    try:
        if d is None:
            return d
        return datetime.strptime(d, DATETIME_FORMAT)
    except Exception as e:
        logging.debug(e)
        logging.debug(f"Failed to parse {d} as datetime")
    return d


TIME_FORMAT = "%H:%M:%S"


def parse_time(d):
    return datetime.strptime(d, TIME_FORMAT).time()


def parse_tdeq(d):
    if "null" in d:
        return None
    try:
        return parse_time(d)
    except Exception as e:
        logging.debug(e)
    return parse_datetime(d)


def parse_progress(progress):
    try:
        return float(progress)
    except Exception as e:
        logging.debug(f"{e} => Fallback to datetime parsing")

    # When finished, progress becomes the date of the end
    if parse_datetime(progress):
        return 100.0
    return None


# https://docs.pydantic.dev/latest/concepts/types/#custom-types
# JobProgress = TypeAliasType('JobProgress', PlainValidator(parse_progress))
Datetime = TypeAliasType(
    "JobProgress", Annotated[datetime, PlainValidator(parse_progress)]
)


def single_xpath(xml, xpath, parser=None, default=None):
    try:
        res = xml.xpath(xpath)
        res = first(res)
    except Exception:
        return default
    if not res:
        return default
    if parser:
        res = parser(res)
    return res


pd = parse_datetime
sx = single_xpath


def mksx(xml):
    def single_xpath(xpath, parser=None, default=None):
        return sx(xml, xpath, parser=parser, default=default)

    return single_xpath


@dataclass
class SoftwareVersion:
    version: str
    filename: str
    released_on: datetime
    downloaded: bool
    current: bool
    latest: bool
    uploaded: bool

    @staticmethod
    def from_xml(xml):
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        p = mksx(xml)
        return SoftwareVersion(
            p("./version/text()"),
            p("./filename/text()"),
            p("./released-on/text()", parser=pd),
            p("./downloaded/text()") != "no",
            p("./current/text()") != "no",
            p("./latest/text()") != "no",
            p("./uploaded/text()") != "no",
        )

    @property
    def base_minor_version(self):
        major, minor, _ = self.version.split(".")
        return f"{major}.{minor}.0"

    @property
    def base_major_version(self):
        major, _, _ = self.version.split(".")
        return f"{major}.0.0"


@dataclass
class Job:
    tenq: datetime
    tdeq: time
    id: str
    user: str
    type: str
    status: str
    queued: bool
    stoppable: bool
    result: str
    tfin: datetime
    description: str
    position_in_queue: int
    progress: float
    details: str
    warnings: str

    @staticmethod
    def from_xml(xml):
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        p = mksx(xml)
        return Job(
            p("./tenq/text()", parser=pd),
            p("./tdeq/text()", parser=parse_tdeq),
            p("./id/text()"),
            p("./user/text()"),
            p("./type/text()"),
            p("./status/text()"),
            p("./queued/text()") != "NO",
            p("./stoppable/text()") != "NO",
            p("./result/text()"),
            p("./tfin/text()", parser=pd),
            p("./description/text()"),
            p("./positionInQ/text()", parser=int),
            p("./progress/text()", parser=parse_progress),
            "\n".join(xml.xpath("./details/line/text()")),
            p("./warnings/text()"),
        )


class Device(BaseModel):
    serial: str
    connected: bool
    unsupported_version: bool
    wildfire_rt: bool
    deactivated: Optional[str] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    ipv6_address: Optional[str] = None
    mac_addr: Optional[str] = None
    uptime: Optional[str] = None
    family: Optional[str] = None
    model: Optional[str] = None
    sw_version: Optional[str] = None
    app_version: Optional[str] = None
    av_version: Optional[str] = None
    device_dictionary_version: Optional[str] = ""
    wildfire_version: Optional[str] = None
    threat_version: Optional[str] = None
    url_db: Optional[str] = None
    url_filtering_version: Optional[str] = None
    logdb_version: Optional[str] = None
    vpnclient_package_version: Optional[str] = None
    global_protect_client_package_version: Optional[str] = None
    prev_app_version: Optional[str] = None
    prev_av_version: Optional[str] = None
    prev_threat_version: Optional[str] = None
    prev_wildfire_version: Optional[str] = None
    prev_device_dictionary_version: Optional[str] = ""
    # domain/: str
    # slot_count: str
    # type/: str
    # tag/: str
    # plugin_versions
    # ha_cluster
    vpn_disable_mode: bool
    operational_mode: str
    certificate_status: Optional[str] = None
    certificate_subject_name: Optional[str] = None
    certificate_expiry: Datetime
    connected_at: Datetime
    custom_certificate_usage: Optional[str] = None
    multi_vsys: bool
    # vsys
    last_masterkey_push_status: str
    last_masterkey_push_timestamp: Optional[str] = None
    express_mode: bool
    device_cert_present: Optional[str] = None
    device_cert_expiry_date: str

    class Config:
        populate_by_name = True
        extra = Extra.allow
        # extra = Extra.ignore

    @staticmethod
    def from_xml(xml):
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        res = {k.replace("-", "_"): v for k, v in el2dict(xml)["entry"].items()}
        return Device(**res)


class VPNFlow(BaseModel):
    name: str
    id: int
    gwid: int
    inner_if: str
    outer_if: str
    localip: str
    peerip: str
    state: str
    mon: str
    owner: str

    class Config:
        populate_by_name = True
        extra = Extra.allow
        # extra = Extra.ignore

    @staticmethod
    def from_xml(xml):
        if isinstance(xml, (list, tuple)):
            xml = first(xml)
        if xml is None:
            return None
        res = {k.replace("-", "_"): v for k, v in el2dict(xml)["entry"].items()}
        return VPNFlow(**res)
