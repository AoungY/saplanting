# -*- coding: utf-8 -*-
from random import random

import mod.client.extraClientApi as clientApi

from .BaseClientSystem import BaseClientSystem
from ..config.heyconfig import ClientSetting
from ..config.sapling import default_saplings
from ..util.common import Singleton
from ..util.listen import Listen

compFactory = clientApi.GetEngineCompFactory()
engineName = clientApi.GetEngineNamespace()
engineSystem = clientApi.GetEngineSystemName()


class ClientMasterSetting(object):
    """
    一个单例类，用于存储和管理从服务端同步过来的主配置。
    这些配置在所有客户端上应该是一致的。
    """
    __metaclass__ = Singleton
    wait_time_range = 5
    check_time_range = 15

    def __init__(self):
        """构造函数，初始化默认配置"""
        self.saplings = default_saplings
        self.min_wait_time = 3
        self.check_min_wait_time = 15 + self.min_wait_time

    def load_config(self, data):
        """
        从字典加载配置。此方法通常在接收到服务端的同步事件时调用。

        :param data: dict, 包含配置信息的字典
        """
        if "saplings" in data:
            self.saplings = set(tuple(value) for value in data["saplings"])
        if "min_wait_time" in data:
            self.min_wait_time = max(0, data["min_wait_time"])
            self.check_min_wait_time = 15 + self.min_wait_time

    def get_wait_time(self):
        """获取一个随机的等待时间（用于树苗落地后通知服务端）"""
        return random() * self.wait_time_range + self.min_wait_time

    def get_check_wait_time(self):
        """获取一个随机的检查间隔时间（用于检查树苗是否落地）"""
        return random() * self.check_time_range + self.check_min_wait_time


class SaplantingClient(BaseClientSystem):
    """
    模组的客户端主System，负责处理所有客户端逻辑。
    包括监听实体事件、处理玩家设置、与服务端通信等。
    """
    def __init__(self, namespace, name):
        super(SaplantingClient, self).__init__(namespace, name)
        self.game_comp = compFactory.CreateGame(self.levelId)
        self.master_setting = ClientMasterSetting()
        self.item_entities = {}  # 追踪世界中的树苗实体
        self.client_setting = ClientSetting()

    @Listen.on("LoadClientAddonScriptsAfter")
    def on_enabled(self, event=None):
        """
        在客户端脚本加载完成后调用的事件。
        用于加载本地配置和注册配置项。
        """
        self.client_setting.load()
        comp = clientApi.CreateComponent(self.levelId, "HeyPixel", "Config")
        if comp:
            from ..config.heyconfig import register_config
            comp.register_config(register_config)

    @Listen.on("UiInitFinished")
    def on_local_player_stop_loading(self, event=None):
        """
        在UI初始化完成后（即玩家进入游戏）调用的事件。
        通知服务端当前玩家的连锁砍树设置状态。
        """
        self.NotifyToServer("SyncPlayerTreeFallingState", {"playerId": self.playerId, "state": self.client_setting.tree_felling})

    def reload_client_setting(self):
        """重新加载客户端本地设置，并通知服务端"""
        self.client_setting.load()
        self.NotifyToServer("SyncPlayerTreeFallingState", {"playerId": self.playerId, "state": self.client_setting.tree_felling})

    @Listen.server("SyncMasterSetting")
    def on_sync_master_setting(self, data):
        """
        监听服务端发来的主配置同步事件。
        """
        self.master_setting.load_config(data)

    @Listen.on("AddEntityClientEvent")
    def on_add_sapling_item(self, event):
        """
        监听实体（这里特指物品）生成事件。
        如果生成的是树苗，则开始追踪它。
        """
        engineTypeStr = event["engineTypeStr"]
        if engineTypeStr == "minecraft:item":
            itemName = event["itemName"]
            auxValue = event["auxValue"]
            item_key = itemName, auxValue
            # 检查物品是否为已定义的树苗
            if item_key in self.master_setting.saplings or "sapling" in itemName:
                entityId = event["id"]
                self.item_entities[entityId] = item_key
                # 启动一个定时器，延迟检查树苗是否已落地
                self.game_comp.AddTimer(self.master_setting.get_check_wait_time(), self.check_on_ground, entityId)

    @Listen.on("RemoveEntityClientEvent")
    def on_remove_entity(self, event):
        """
        监听实体移除事件。
        如果被移除的实体是正在追踪的树苗，则停止追踪。
        """
        entityId = event["id"]
        if entityId in self.item_entities:
            self.item_entities.pop(entityId)

    @Listen.on("OnGroundClientEvent")
    def on_sapling_on_ground(self, event):
        """
        监听实体落地事件。
        如果落地的实体是正在追踪的树苗，则准备通知服务端。
        """
        entityId = event["id"]
        if entityId in self.item_entities:
            # 启动一个短暂的定时器再通知，避免过于频繁或瞬间完成，让其更自然
            self.game_comp.AddTimer(self.master_setting.get_wait_time(), self.on_ground_notify, entityId)

    def on_ground_notify(self, entityId):
        """
        延迟后，实际通知服务端树苗已落地。
        """
        if entityId in self.item_entities:
            itemName, auxValue = self.item_entities[entityId]
            self.NotifyToServer("onSaplingOnGround", {"playerId": self.playerId, "entityId": entityId, "itemName": itemName, "auxValue": auxValue})

    def check_on_ground(self, entityId):
        """
        定时检查一个实体是否在地面上。
        这是对 OnGroundClientEvent 的一个补充和保障。
        """
        if entityId in self.item_entities:
            if compFactory.CreateAttr(entityId).isEntityOnGround():
                self.on_ground_notify(entityId)
            else:
                # 如果还没落地，则再设置一个定时器继续检查
                self.game_comp.AddTimer(self.master_setting.get_check_wait_time(), self.check_on_ground, entityId)

    def reload_master_setting(self):
        """通知服务端，请求重新加载并同步主配置"""
        self.NotifyToServer("ReloadMasterSetting", {})
