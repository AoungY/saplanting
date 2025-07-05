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
    __metaclass__ = Singleton
    wait_time_range = 5
    check_time_range = 15

    def __init__(self):
        self.saplings = default_saplings
        self.min_wait_time = 3
        self.check_min_wait_time = 15 + self.min_wait_time

    def load_config(self, data):
        if "saplings" in data:
            self.saplings = set(tuple(value) for value in data["saplings"])
        if "min_wait_time" in data:
            self.min_wait_time = max(0, data["min_wait_time"])
            self.check_min_wait_time = 15 + self.min_wait_time

    def get_wait_time(self):
        return random() * self.wait_time_range + self.min_wait_time

    def get_check_wait_time(self):
        return random() * self.check_time_range + self.check_min_wait_time


class SaplantingClient(BaseClientSystem):
    def __init__(self, namespace, name):
        super(SaplantingClient, self).__init__(namespace, name)
        self.game_comp = compFactory.CreateGame(self.levelId)
        self.master_setting = ClientMasterSetting()
        self.item_entities = {}
        self.client_setting = ClientSetting()

    @Listen.on("LoadClientAddonScriptsAfter")
    def on_enabled(self, event=None):
        self.client_setting.load()
        comp = clientApi.CreateComponent(self.levelId, "HeyPixel", "Config")
        if comp:
            from ..config.heyconfig import register_config
            comp.register_config(register_config)

    @Listen.on("UiInitFinished")
    def on_local_player_stop_loading(self, event=None):
        self.NotifyToServer("SyncPlayerTreeFallingState", {"playerId": self.playerId, "state": self.client_setting.tree_felling})

    def reload_client_setting(self):
        self.client_setting.load()
        self.NotifyToServer("SyncPlayerTreeFallingState", {"playerId": self.playerId, "state": self.client_setting.tree_felling})

    @Listen.server("SyncMasterSetting")
    def on_sync_master_setting(self, data):
        self.master_setting.load_config(data)

    @Listen.on("AddEntityClientEvent")
    def on_add_sapling_item(self, event):
        engineTypeStr = event["engineTypeStr"]
        if engineTypeStr == "minecraft:item":
            itemName = event["itemName"]
            auxValue = event["auxValue"]
            item_key = itemName, auxValue
            if item_key in self.master_setting.saplings or "sapling" in itemName:
                entityId = event["id"]
                self.item_entities[entityId] = item_key
                self.game_comp.AddTimer(self.master_setting.get_check_wait_time(), self.check_on_ground, entityId)

    @Listen.on("RemoveEntityClientEvent")
    def on_remove_entity(self, event):
        entityId = event["id"]
        if entityId in self.item_entities:
            self.item_entities.pop(entityId)

    @Listen.on("OnGroundClientEvent")
    def on_sapling_on_ground(self, event):
        entityId = event["id"]
        if entityId in self.item_entities:
            self.game_comp.AddTimer(self.master_setting.get_wait_time(), self.on_ground_notify, entityId)

    def on_ground_notify(self, entityId):
        if entityId in self.item_entities:
            itemName, auxValue = self.item_entities[entityId]
            # print "notify sapling item on ground", entityId
            self.NotifyToServer("onSaplingOnGround", {"playerId": self.playerId, "entityId": entityId, "itemName": itemName, "auxValue": auxValue})

    def check_on_ground(self, entityId):
        if entityId in self.item_entities:
            if compFactory.CreateAttr(entityId).isEntityOnGround():
                self.on_ground_notify(entityId)
            else:
                self.game_comp.AddTimer(self.master_setting.get_check_wait_time(), self.check_on_ground, entityId)

    def reload_master_setting(self):
        self.NotifyToServer("ReloadMasterSetting", {})
