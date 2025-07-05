# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:14
# @Author  : taokyla
# @File    : client.py

import mod.client.extraClientApi as clientApi

from .base import SavableConfig
from ...util.common import dealunicode, Singleton

compFactory = clientApi.GetEngineCompFactory()

configComp = compFactory.CreateConfigClient(clientApi.GetLevelId())


class ClientSavableConfig(SavableConfig):
    __metaclass__ = Singleton
    _ISGLOBAL = False

    def load(self):
        data = dealunicode(configComp.GetConfigData(self._KEY, self._ISGLOBAL))
        if data:
            self.load_data(data)

    def save(self):
        configComp.SetConfigData(self._KEY, self.dump(), isGlobal=self._ISGLOBAL)
