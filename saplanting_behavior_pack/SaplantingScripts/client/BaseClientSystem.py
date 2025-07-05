# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

from ..config.modConfig import *
from ..util.listen import Listen

engineName = clientApi.GetEngineNamespace()
engineSystem = clientApi.GetEngineSystemName()


class BaseClientSystem(clientApi.GetClientSystemCls()):
    ListenDict = {Listen.minecraft: (engineName, engineSystem), Listen.client: (ModName, ClientSystemName), Listen.server: (ModName, ServerSystemName)}

    def __init__(self, namespace, name):
        super(BaseClientSystem, self).__init__(namespace, name)
        self.levelId = clientApi.GetLevelId()
        self.playerId = clientApi.GetLocalPlayerId()
        self.onRegister()

    def onRegister(self):
        for key in dir(self):
            obj = getattr(self, key)
            if callable(obj) and hasattr(obj, 'listen_event'):
                event = getattr(obj, "listen_event")
                _type = getattr(obj, "listen_type")
                priority = getattr(obj, "listen_priority")
                self.listen(event, obj, _type=_type, priority=priority)

    def listen(self, event, func, _type=Listen.minecraft, priority=0):
        if _type not in self.ListenDict:
            return
        name, system = self.ListenDict[_type]
        self.ListenForEvent(name, system, event, self, func, priority=priority)

    def unlisten(self, event, func, _type=Listen.minecraft, priority=0):
        if _type not in self.ListenDict:
            return
        name, system = self.ListenDict[_type]
        self.UnListenForEvent(name, system, event, self, func, priority=priority)
