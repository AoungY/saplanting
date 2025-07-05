# -*- coding: utf-8 -*-
from ..base_event import BaseEvent


class ClientChestCloseEvent(BaseEvent):
    """
    关闭箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子
    """
    pass


class ClientChestOpenEvent(BaseEvent):
    """
    开启箱子界面时触发，包括小箱子，合并后大箱子和末影龙箱子
    """
    playerId = None  # type: str
    """玩家实体id"""
    x = None  # type: int
    """箱子位置x值"""
    y = None  # type: int
    """箱子位置y值"""
    z = None  # type: int
    """箱子位置z值"""


class ClientPlayerInventoryCloseEvent(BaseEvent):
    """关闭物品背包界面时触发"""
    pass


class ClientPlayerInventoryOpenEvent(BaseEvent):
    """打开物品背包界面时触发"""
    isCreative = None  # type: bool
    """是否是创造模式背包界面"""
    cancel = None  # type: bool
    """取消打开物品背包界面"""


class GridComponentSizeChangedClientEvent(BaseEvent):
    """触发时机：UI grid组件里格子数目发生变化时触发"""
    pass


class OnItemSlotButtonClickedEvent(BaseEvent):
    """
    点击快捷栏和背包栏的物品槽时触发
    """
    slotIndex = None  # type: int
    """点击的物品槽的编号"""


class PlayerChatButtonClickClientEvent(BaseEvent):
    """玩家点击聊天按钮或回车键触发呼出聊天窗口时客户端抛出的事件"""
    pass


class PopScreenEvent(BaseEvent):
    """
    screen移除触发
    """
    screenName = None  # type: str
    """UI名字"""


class PushScreenEvent(BaseEvent):
    """
    screen创建触发
    """
    screenName = None  # type: str
    """UI名字"""


class UiInitFinished(BaseEvent):
    """UI初始化框架完成,此时可以创建UI"""
    pass
