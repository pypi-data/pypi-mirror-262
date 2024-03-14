import ipih

from pih.tools import lnk
from pih.consts import LINK
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "ws735"

HOST = Hosts.WS735

MODULES: tuple[str, ...] = ("pywin32", "Pillow")

VERSION: str = "0.11"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="ws-735 service",
    host=HOST.NAME,
    login=lnk(LINK.DEVELOPER_LOGIN),
    password=lnk(LINK.DEVELOPER_PASSWORD),
    commands=("print_image",),
    host_changeable=False,
    standalone_name="ws735",
    version=VERSION,
    packages=MODULES,
)
