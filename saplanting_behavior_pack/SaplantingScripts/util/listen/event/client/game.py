# -*- coding: utf-8 -*-
from ..base_event import BaseEvent


class AddEntityClientEvent(BaseEvent):
    """客户端侧创建新实体时触发
    """
    id = None  # type: str
    """实体id"""
    posX = None  # type: float
    """位置x"""
    posY = None  # type: float
    """位置y"""
    posZ = None  # type: float
    """位置z"""
    dimensionId = None  # type: int
    """实体维度"""
    isBaby = None  # type: bool
    """是否为幼儿"""
    engineTypeStr = None  # type: str
    """实体类型"""
    itemName = None  # type: str
    """物品identifier（仅当物品实体时存在该字段）"""
    auxValue = None  # type: int
    """物品附加值（仅当物品实体时存在该字段）"""


class AddPlayerAOIClientEvent(BaseEvent):
    """
    玩家加入游戏或者其余玩家进入当前玩家所在的区块时触发的AOI事件，替换AddPlayerEvent
    """
    playerId = None  # type:  str
    """玩家id"""


class ChunkAcquireDiscardedClientEvent(BaseEvent):
    """
    触发时机：客户端区块即将被卸载时
    """
    dimension = None  # type: int
    """区块所在维度"""
    chunkPosX = None  # type: int
    """区块的x坐标，对应方块X坐标区间为[x * 16, x * 16 + 15]"""
    chunkPosZ = None  # type: int
    """区块的z坐标，对应方块Z坐标区间为[z * 16, z * 16 + 15]"""


class ChunkLoadedClientEvent(BaseEvent):
    """
    触发时机：客户端区块加载完成时
    """
    dimension = None  # type: int
    """区块所在维度"""
    chunkPosX = None  # type: int
    """区块的x坐标，对应方块X坐标区间为[x * 16, x * 16 + 15]"""
    chunkPosZ = None  # type: int
    """区块的z坐标，对应方块Z坐标区间为[z * 16, z * 16 + 15]"""
    pass

class ClientChatEvent(BaseEvent):
    """
    客户端聊天事件
    """
    username = None  # type: str
    """玩家名称"""
    playerId = None  # type: str
    """玩家id"""
    message = None  # type: str
    """玩家发送的聊天消息内容"""
    cancel = None  # type: bool
    """是否取消这个聊天事件，若取消可以设置为True"""

class LoadClientAddonScriptsAfter(BaseEvent):
    """客户端加载mod完成事件"""
    pass


class OnCommandOutputClientEvent(BaseEvent):
    """
    当command命令有成功消息输出时触发
    """

    command = None  # type: str
    """命令名称"""
    message = None  # type: str
    """命令返回的消息"""


class OnLocalPlayerStopLoading(BaseEvent):
    """
    触发时机：玩家进入存档，出生点地形加载完成时触发。该事件触发时可以进行切换维度的操作
    """
    playerId = None  # type:  str
    """加载完成的玩家id"""


class OnScriptTickClient(BaseEvent):
    """客户端tick事件,1秒30次"""
    pass


class RemoveEntityClientEvent(BaseEvent):
    """客户端侧实体被移除时触发"""
    id = None  # type:  str
    """移除的实体id"""


class RemovePlayerAOIClientEvent(BaseEvent):
    """
    玩家离开当前玩家同一个区块时触发AOI事件
    """
    playerId = None  # type:  str
    """玩家id"""


class UnLoadClientAddonScriptsBefore(BaseEvent):
    """客户端卸载mod之前触发"""
    pass
