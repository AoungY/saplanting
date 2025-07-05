# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:14
# @Author  : taokyla
# @File    : client.py

import mod.client.extraClientApi as clientApi

from .base import SavableConfig
from ...util.common import dealunicode, Singleton

# 获取引擎的组件工厂
compFactory = clientApi.GetEngineCompFactory()

# 创建一个客户端配置组件的实例，用于读写本地配置文件
configComp = compFactory.CreateConfigClient(clientApi.GetLevelId())


class ClientSavableConfig(SavableConfig):
    """
    客户端可持久化配置的实现类。
    继承自SavableConfig，并使用客户端API来实现具体的load和save方法。
    使用了单例模式，确保每个配置类在运行时只有一个实例。
    """
    __metaclass__ = Singleton
    # 配置是否为全局配置（True）或当前存档特定的配置（False）
    _ISGLOBAL = False

    def load(self):
        """
        从游戏本地存储中加载配置数据。
        它通过引擎的ConfigClient组件读取数据，并使用父类的load_data方法来填充实例属性。
        """
        # dealunicode用于处理从引擎读出的数据可能存在的编码问题
        data = dealunicode(configComp.GetConfigData(self._KEY, self._ISGLOBAL))
        if data:
            self.load_data(data)

    def save(self):
        """
        将当前配置数据保存到游戏本地存储中。
        它调用父类的dump方法将配置序列化为字典，然后通过引擎的ConfigClient组件写入数据。
        """
        configComp.SetConfigData(self._KEY, self.dump(), isGlobal=self._ISGLOBAL)
