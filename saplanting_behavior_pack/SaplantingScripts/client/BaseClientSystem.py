# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from ..config.modConfig import *
from ..util.listen import Listen

engineName = clientApi.GetEngineNamespace()
engineSystem = clientApi.GetEngineSystemName()


class BaseClientSystem(clientApi.GetClientSystemCls()):
    """
    客户端System的基类，提供事件自动注册和监听的通用功能。
    所有客户端的System都应继承自此类，以简化事件处理。
    """
    ListenDict = {Listen.minecraft: (engineName, engineSystem), Listen.client: (ModName, ClientSystemName), Listen.server: (ModName, ServerSystemName)}
    """事件监听字典，用于映射不同类型的事件源到对应的命名空间和系统名"""

    def __init__(self, namespace, name):
        """
        构造函数，在客户端系统初始化时调用。

        :param namespace: 客户端系统的命名空间
        :param name: 客户端系统的名称
        """
        super(BaseClientSystem, self).__init__(namespace, name)
        self.levelId = clientApi.GetLevelId()
        self.playerId = clientApi.GetLocalPlayerId()
        self.onRegister()

    def onRegister(self):
        """
        自动注册事件监听器。
        该方法会遍历类的所有方法，如果一个方法被特定的装饰器（如@listen_event）标记过，
        就会自动将其注册为游戏事件的监听函数。
        """
        for key in dir(self):
            obj = getattr(self, key)
            if callable(obj) and hasattr(obj, 'listen_event'):
                event = getattr(obj, "listen_event")
                _type = getattr(obj, "listen_type")
                priority = getattr(obj, "listen_priority")
                self.listen(event, obj, _type=_type, priority=priority)

    def listen(self, event, func, _type=Listen.minecraft, priority=0):
        """
        注册一个事件监听。

        :param event: str, 要监听的事件名称
        :param func: function, 事件触发时调用的回调函数
        :param _type: Listen, 事件类型（minecraft, client, server），默认为minecraft原生事件
        :param priority: int, 监听器的优先级
        """
        if _type not in self.ListenDict:
            return
        name, system = self.ListenDict[_type]
        self.ListenForEvent(name, system, event, self, func, priority=priority)

    def unlisten(self, event, func, _type=Listen.minecraft, priority=0):
        """
        取消一个事件监听。

        :param event: str, 要取消监听的事件名称
        :param func: function, 要取消的回调函数
        :param _type: Listen, 事件类型
        :param priority: int, 监听器的优先级
        """
        if _type not in self.ListenDict:
            return
        name, system = self.ListenDict[_type]
        self.UnListenForEvent(name, system, event, self, func, priority=priority)
