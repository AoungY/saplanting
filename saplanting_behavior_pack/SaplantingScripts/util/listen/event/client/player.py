# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class ApproachEntityClientEvent(BaseEvent):
    """玩家靠近生物时触发"""
    playerId = None  # type: str
    """玩家实体id"""
    entityId = None  # type: str
    """靠近的生物实体id"""


class LeaveEntityClientEvent(BaseEvent):
    """玩家远离生物时触发"""
    playerId = None  # type: str
    """玩家实体id"""
    entityId = None  # type: str
    """远离的生物实体id"""


class DimensionChangeClientEvent(BaseEvent):
    """玩家维度改变时客户端抛出

    当通过传送门从末地回到主世界时，toY值为32767，其他情况一般会比设置值高1.62
    """
    playerId = None  # type: str
    """玩家实体id"""
    fromDimensionId = None  # type: int
    """维度改变前的维度"""
    toDimensionId = None  # type: int
    """维度改变后的维度"""
    fromX = None  # type: float
    """改变前的位置x"""
    fromY = None  # type: float
    """改变前的位置Y"""
    fromZ = None  # type: float
    """改变前的位置Z"""
    toX = None  # type: float
    """改变后的位置x"""
    toY = None  # type: float
    """改变后的位置Y"""
    toZ = None  # type: float
    """改变后的位置Z"""


class DimensionChangeFinishClientEvent(BaseEvent):
    """玩家维度改变完成后客户端抛出
    当通过传送门从末地回到主世界时，toPos的y值为32767，其他情况一般会比设置值高1.62
    """
    playerId = None  # type: str
    """玩家实体id"""
    fromDimensionId = None  # type: int
    """维度改变前的维度"""
    toDimensionId = None  # type: int
    """维度改变后的维度"""
    toPos = None  # type: tuple[float,float,float]
    """改变后的位置x,y,z,其中y值为脚底加上角色的身高值"""


class ExtinguishFireClientEvent(BaseEvent):
    """
    玩家扑灭火焰时触发。下雨，倒水等方式熄灭火焰不会触发。
    """
    pos = None  # type: tuple[float,float,float]
    """火焰方块的坐标"""
    playerId = None  # type: str
    """玩家id"""
    cancel = None  # type: bool
    """修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireServerEvent一起修改。"""


class GameTypeChangedClientEvent(BaseEvent):
    """个人游戏模式发生变化时客户端触发。
    游戏模式：GetMinecraftEnum().GameType.*:Survival，Creative，Adventure分别为0~2 默认游戏模式发生变化时最后反映在个人游戏模式之上。
    """
    playerId = None  # type: str
    """玩家Id"""
    oldGameType = None  # type: int
    """切换前的游戏模式"""
    newGameType = None  # type: int
    """切换后的游戏模式"""


class OnPlayerHitBlockClientEvent(BaseEvent):
    """
    触发时机：通过OpenPlayerHitBlockDetection打开方块碰撞检测后，当玩家碰撞到方块时触发该事件。玩家着地时会触发OnGroundClientEvent，而不是该事件。客户端和服务端分别作碰撞检测，可能两个事件返回的结果略有差异。
    """
    playerId = None  # type: str
    """碰撞到方块的玩家Id"""
    posX = None  # type: int
    """碰撞方块x坐标"""
    posY = None  # type: int
    """碰撞方块y坐标"""
    posZ = None  # type: int
    """碰撞方块z坐标"""
    blockId = None  # type: str
    """碰撞方块的identifier"""
    auxValue = None  # type: int
    """碰撞方块的附加值"""


class OnPlayerHitMobClientEvent(BaseEvent):
    """
    触发时机：通过OpenPlayerHitMobDetection打开生物碰撞检测后，当有生物与玩家碰撞时触发该事件。注：客户端和服务端分别作碰撞检测，可能两个事件返回的结果略有差异。
    """
    playerList = None  # type: list[str]
    """生物碰撞到的玩家id的list"""


class PerspChangeClientEvent(BaseEvent):
    """视角切换时会触发的事件
    视角数字代表含义 0: 第一人称 1: 第三人称背面 2: 第三人称正面
    """
    _from = None  # type: int
    """切换前的视角"""
    to = None  # type: int
    """切换后的视角"""

    def __getattribute__(self, name):
        if name == '_from':
            return self.__dict__['from']
        return super(PerspChangeClientEvent, self).__getattribute__(name)

    def __setattr__(self, name, value):
        if name == '_from':
            self.__dict__['from'] = value
        else:
            super(PerspChangeClientEvent, self).__setattr__(name, value)
