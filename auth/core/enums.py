from enum import Enum


class Action(Enum):
    login = "login"
    logout = "logout"


class DeviceType(Enum):
    pc = "pc"
    mobile = "mobile"
    tablet = "tablet"
    undefined = "undefined"
