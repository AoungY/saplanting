# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class AttackAnimBeginClientEvent(BaseEvent):
    """攻击动作开始时触发

    使用SetModel替换骨骼模型后，该事件才生效
    """
    id = None  # type: str
    """实体id"""


class AttackAnimEndClientEvent(BaseEvent):
    """攻击动作结束时触发

    使用SetModel替换骨骼模型后，该事件才生效
    """
    id = None  # type: str
    """实体id"""


class WalkAnimBeginClientEvent(BaseEvent):
    """走路动作开始时触发

    使用SetModel替换骨骼模型后，该事件才生效
    """
    id = None  # type: str
    """实体id"""


class WalkAnimEndClientEvent(BaseEvent):
    """走路动作结束时触发

    使用SetModel替换骨骼模型后，该事件才生效
    """
    id = None  # type: str
    """实体id"""