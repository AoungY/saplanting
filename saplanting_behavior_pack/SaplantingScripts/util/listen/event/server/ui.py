# -*- coding: utf-8 -*-
from ..base_event import BaseEvent


class PlayerInventoryOpenScriptServerEvent(BaseEvent):
    """
    某个客户端打开物品背包界面时触发
    """
    playerId = None  # type: str
    """玩家实体id"""
    isCreative = None  # type bool
    """是否背包界面"""
