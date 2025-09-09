import os
from enum import Enum

"""
    alarm level enum
"""
class AlarmLevel(Enum):
    NORMAL = ("NORMAL", "<font>", "</font>")
    URGENT = ("URGENT", '<font color="warning">', "</font>")
    CRITICAL = ("CRITICAL", '<font color="red">**', "**</font>")
    DISASTER = ("DISASTER", '<font color="red">**', "**</font>")

    def __init__(self, desc: str, tag_start: str, tag_end: str):
        self.desc = desc
        self.tag_start = tag_start
        self.tag_end = tag_end

    @classmethod
    def get_by_key(cls, key: str) -> "AlarmLevel | None":
        return cls.__members__.get(key)


"""
    list of enterprise wechat robot templates
"""
class WechatRobotEnum(Enum):
    DEFAULT = ("", "default robot")

    def __init__(self, robot_name: str, desc: str):
        self.robot_name = robot_name
        self.desc = desc

    @classmethod
    def get_by_key(cls, key: str) -> "WechatRobotEnum | None":
        return cls.__members__.get(key)

"""
test environment identification
"""
TEST_ENV = "test"

"""
app environment
"""
APP_ENV = os.getenv("APP_ENV", TEST_ENV)