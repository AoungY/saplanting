# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:15
# @Author  : taokyla
# @File    : server.py
import mod.server.extraServerApi as serverApi

from .base import SavableConfig
from ...util.common import dealunicode, Singleton

# 获取引擎的组件工厂
compFactory = serverApi.GetEngineCompFactory()

# 创建一个全局的附加数据组件实例，用于读写与当前存档（Level）相关的全局数据
extraDataComp = compFactory.CreateExtraData(serverApi.GetLevelId())


class ServerSavableConfig(SavableConfig):
    """
    服务端全局可持久化配置的实现类。
    它用于存储不与任何特定玩家绑定，而是与整个服务器/存档相关的配置。
    使用了单例模式，确保每个全局配置类在运行时只有一个实例。
    """
    __metaclass__ = Singleton

    def load(self):
        """
        从服务端的全局附加数据中加载配置。
        """
        data = dealunicode(extraDataComp.GetExtraData(self._KEY))
        if data:
            self.load_data(data)

    def save(self):
        """
        将当前配置保存到服务端的全局附加数据中。
        """
        extraDataComp.SetExtraData(self._KEY, self.dump(), autoSave=True)
        extraDataComp.SaveExtraData()


class PlayerSavableConfig(SavableConfig):
    """
    与特定玩家绑定的可持久化配置的实现类。
    注意：此类【不是】单例，每个实例都对应一个玩家。
    """

    def __init__(self, playerId):
        """
        构造函数。
        :param playerId: str, 该配置实例所关联的玩家ID
        """
        self._playerId = playerId
        # 为特定玩家创建一个附加数据组件实例，后续的读写都将针对该玩家
        self._extraDataComp = compFactory.CreateExtraData(playerId)

    @property
    def playerId(self):
        """获取当前配置实例关联的玩家ID。"""
        return self._playerId

    def load(self):
        """
        从当前玩家的附加数据中加载配置。
        """
        data = dealunicode(self._extraDataComp.GetExtraData(self._KEY))
        if data:
            self.load_data(data)

    def save(self):
        """
        将当前配置保存到当前玩家的附加数据中。
        """
        self._extraDataComp.SetExtraData(self._KEY, self.dump(), autoSave=True)
        self._extraDataComp.SaveExtraData()
