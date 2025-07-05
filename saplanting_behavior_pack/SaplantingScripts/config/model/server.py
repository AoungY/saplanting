# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:15
# @Author  : taokyla
# @File    : server.py
import mod.server.extraServerApi as serverApi

from .base import SavableConfig
from ...util.common import dealunicode, Singleton

compFactory = serverApi.GetEngineCompFactory()

extraDataComp = compFactory.CreateExtraData(serverApi.GetLevelId())


class ServerSavableConfig(SavableConfig):
    __metaclass__ = Singleton

    def load(self):
        data = dealunicode(extraDataComp.GetExtraData(self._KEY))
        if data:
            self.load_data(data)

    def save(self):
        extraDataComp.SetExtraData(self._KEY, self.dump(), autoSave=True)
        extraDataComp.SaveExtraData()


class PlayerSavableConfig(SavableConfig):

    def __init__(self, playerId):
        self._playerId = playerId
        self._extraDataComp = compFactory.CreateExtraData(playerId)

    @property
    def playerId(self):
        return self._playerId

    def load(self):
        data = dealunicode(self._extraDataComp.GetExtraData(self._KEY))
        if data:
            self.load_data(data)

    def save(self):
        self._extraDataComp.SetExtraData(self._KEY, self.dump(), autoSave=True)
        self._extraDataComp.SaveExtraData()
