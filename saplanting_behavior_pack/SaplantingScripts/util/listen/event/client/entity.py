# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class ApproachEntityClientEvent(BaseEvent):
    """
    玩家靠近生物时触发
    """
    playerId = None  # type: str
    """玩家实体id"""
    entityId = None  # type: str
    """靠近的生物实体id"""


class EntityModelChangedClientEvent(BaseEvent):
    """
    触发时机：实体模型切换时触发
    """
    entityId = None  # type: str
    """实体id"""
    newModel = None  # type: str
    """新的模型名字"""
    oldModel = None  # type: str
    """原来的模型名字"""


class EntityStopRidingEvent(BaseEvent):
    """触发时机：当实体停止骑乘时
    以下情况不允许取消
        - ride组件StopEntityRiding接口
        - 玩家传送时
        - 坐骑死亡时
        - 玩家睡觉时
        - 玩家死亡时
        - 未驯服的马
        - 怕水的生物坐骑进入水里
        - 切换维度
    """
    id = None  # type: str
    """实体id"""
    rideId = None  # type: str
    """坐骑id"""
    exitFromRider = None  # type: bool
    """是否下坐骑"""
    entityIsBeingDestroyed = None  # type: bool
    """坐骑是否将要销毁"""
    switchingRides = None  # type: bool
    """是否换乘坐骑"""
    cancel = None  # type: bool
    """设置为True可以取消（需要与服务端事件一同取消）"""


class HealthChangeClientEvent(BaseEvent):
    """
    生物生命值发生变化时触发
    """

    entityId = None  # type: str
    """实体id"""
    _from = None  # type: float
    """变化前的生命值"""
    to = None  # type: float
    """变化后的生命值"""

    def __getattribute__(self, name):
        if name == '_from':
            return self.__dict__['from']
        return super(HealthChangeClientEvent, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if name == '_from':
            self.__dict__['from'] = value
        else:
            super(HealthChangeClientEvent, self).__setattr__(name, value)


class LeaveEntityClientEvent(BaseEvent):
    """玩家远离生物时触发"""
    playerId = None  # type: str
    """玩家实体id"""
    entityId = None  # type: str
    """远离的生物实体id"""


class OnGroundClientEvent(BaseEvent):
    """
    实体着地事件。玩家，沙子，铁砧，掉落的物品，点燃的TNT掉落地面时触发，其余实体着地不触发。

    - id : str 实体id

    """
    pass


class StartRidingClientEvent(BaseEvent):
    """
    触发时机：一个实体即将骑乘另外一个实体
    """
    cancel = None  # type: bool
    """是否允许触发，默认为False，若设为True，可阻止触发后续的实体交互事件"""
    actorId = None  # type: str
    """骑乘者的唯一ID"""
    victimId = None  # type: str
    """被骑乘实体的唯一ID"""
    pass