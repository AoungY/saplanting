# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class AttackAnimBeginServerEvent(BaseEvent):
    """当攻击动作开始时触发

    - id : str 实体id

    使用SetModel替换骨骼模型后，该事件才生效
    """
    pass


class AttackAnimEndServerEvent(BaseEvent):
    """当攻击动作结束时触发

    - id : str 实体id

    使用SetModel替换骨骼模型后，该事件才生效
    """
    pass


class JumpAnimBeginServerEvent(BaseEvent):
    """当跳跃动作开始时触发

    - id : str 实体id

    使用SetModel替换骨骼模型后，该事件才生效
    """
    pass


class WalkAnimBeginServerEvent(BaseEvent):
    """当走路动作开始时触发

    - id : str 实体id

    使用SetModel替换骨骼模型后，该事件才生效
    """
    pass


class WalkAnimEndServerEvent(BaseEvent):
    """当走路动作结束时触发

    - id : str 实体id

    使用SetModel替换骨骼模型后，该事件才生效
    """
    pass
