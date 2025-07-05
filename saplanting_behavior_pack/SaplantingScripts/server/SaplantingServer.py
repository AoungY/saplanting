# -*- coding: utf-8 -*-
import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import ItemPosType, Facing

from .BaseServerSystem import BaseServerSystem
from ..config.heyconfig_server import MasterSetting
from ..config.sapling import special_saplings, BLOCKSURROUNDINGS, LEAVE_BLOCKS
from ..util.common import get_block_pos
from ..util.listen import Listen, ServerChatEvent, DelServerPlayerEvent
from ..util.server_util import isAxe

compFactory = serverApi.GetEngineCompFactory()


class SaplantingServer(BaseServerSystem):

    def __init__(self, namespace, name):
        super(SaplantingServer, self).__init__(namespace, name)
        self.masterId = None
        self.player_tree_falling_state = {}  # type: dict[str,bool]
        self.player_destroying = {}  # type: dict[str,set]
        self.game_comp = compFactory.CreateGame(self.levelId)
        self.item_comp = compFactory.CreateItem(self.levelId)
        self.msg_comp = compFactory.CreateMsg(self.levelId)
        self.block_info_comp = compFactory.CreateBlockInfo(self.levelId)
        self.block_state_comp = compFactory.CreateBlockState(self.levelId)
        self.master_setting = MasterSetting()
        self.master_setting.load()

    @Listen.on("OnCarriedNewItemChangedServerEvent")
    def on_player_hand_item_change(self, event):
        if not self.master_setting.tree_felling:
            return
        newItemDict = event["newItemDict"]
        if newItemDict and isAxe(newItemDict["newItemName"], newItemDict["newAuxValue"]):
            playerId = event["playerId"]
            state = self.player_tree_falling_state.get(playerId, False)
            self.game_comp.SetOneTipMessage(playerId, "连锁砍树:{}".format("§a开" if state else "§c关"))

    @Listen.client("SyncPlayerTreeFallingState")
    def on_sync_player_tree_falling_state(self, event):
        playerId = event["__id__"] if "__id__" in event else event["playerId"]
        self.player_tree_falling_state[playerId] = event["state"]

    @Listen.on(ServerChatEvent)
    def on_command(self, event):
        playerId = event["playerId"]
        if playerId == self.masterId:
            message = event["message"].lower()
            if message == "#hpldsg":
                event["cancel"] = True
                handItem = compFactory.CreateItem(playerId).GetPlayerItem(ItemPosType.CARRIED)
                if not handItem:
                    self.msg_comp.NotifyOneMessage(playerId, "§a[落地生根]§c没有物品在手上，添加失败")
                    return
                item_key = handItem["newItemName"], handItem["newAuxValue"]
                if item_key not in self.master_setting.saplings:
                    self.master_setting.saplings.add(item_key)
                    self.master_setting.save()
                    data = self.master_setting.get_client_data(add_min_wait_time=False)
                    self.BroadcastToAllClient("SyncMasterSetting", data)
                    self.msg_comp.NotifyOneMessage(playerId, "§a[落地生根]§a添加方块{}:{}到白名单成功".format(*item_key))
                else:
                    self.master_setting.saplings.discard(item_key)
                    self.master_setting.save()
                    data = self.master_setting.get_client_data(add_min_wait_time=False)
                    self.BroadcastToAllClient("SyncMasterSetting", data)
                    self.msg_comp.NotifyOneMessage(playerId, "§a[落地生根]§a方块{}:{}已移出白名单".format(*item_key))
            elif message == "#hpldsgmt":
                event["cancel"] = True
                handItem = compFactory.CreateItem(playerId).GetPlayerItem(ItemPosType.CARRIED)
                if not handItem:
                    self.msg_comp.NotifyOneMessage(playerId, "§a[落地生根]§c没有物品在手上，添加失败")
                    return
                item_name = handItem["newItemName"]
                if item_name not in self.master_setting.log_blocks:
                    self.master_setting.log_blocks.add(item_name)
                    self.master_setting.save()
                    self.msg_comp.NotifyOneMessage(playerId, "§a[落地生根]§a已添加方块{}为木头，忽略子id".format(item_name))
                else:
                    self.master_setting.log_blocks.discard(item_name)
                    self.master_setting.save()
                    self.msg_comp.NotifyOneMessage(playerId, "§a[落地生根]§a已取消将方块{}识别为木头".format(item_name))

    @Listen.client("ReloadMasterSetting")
    def on_reload_master_setting(self, event=None):
        self.master_setting.load()
        data = self.master_setting.get_client_data(add_saplings=False)
        self.BroadcastToAllClient("SyncMasterSetting", data)

    @Listen.on("LoadServerAddonScriptsAfter")
    def on_enabled(self, event=None):
        comp = serverApi.CreateComponent(self.levelId, "HeyPixel", "Config")
        if comp:
            from ..config.heyconfig_server import register_config_server
            comp.register_config(register_config_server)

    @Listen.on("ClientLoadAddonsFinishServerEvent")
    def on_player_login_finish(self, event):
        playerId = event["playerId"]
        if self.masterId is None:
            self.masterId = playerId
        self.player_destroying[playerId] = set()
        self.NotifyToClient(playerId, "SyncMasterSetting", self.master_setting.get_client_data())

    @Listen.on(DelServerPlayerEvent)
    def on_player_leave(self, event):
        playerId = event["id"]
        if playerId in self.player_destroying:
            self.player_destroying.pop(playerId)

    @Listen.client("onSaplingOnGround")
    def on_sapling_on_ground(self, event):
        # print "receive sapling on ground", event
        playerId = event["__id__"] if "__id__" in event else event["playerId"]
        entityId = event["entityId"]
        if not self.game_comp.IsEntityAlive(entityId):
            # print "entity not exists"
            return
        dim = compFactory.CreateDimension(entityId).GetEntityDimensionId()
        item_entity_pos = compFactory.CreatePos(entityId).GetFootPos()
        entityId_block_pos = get_block_pos(item_entity_pos)
        block = self.block_info_comp.GetBlockNew(entityId_block_pos, dimensionId=dim)
        if block:
            if block["name"] == "minecraft:farmland":
                entityId_block_pos = entityId_block_pos[0], entityId_block_pos[1] + 1, entityId_block_pos[2]
                block = self.block_info_comp.GetBlockNew(entityId_block_pos, dimensionId=dim)
                if not block:
                    return
            if block["name"] not in {"minecraft:air", "minecraft:water", "minecraft:flowing_water"}:
                return
        itemName = event["itemName"]
        auxValue = event["auxValue"]
        item_key = itemName, auxValue
        if item_key in special_saplings:
            itemName, auxValue = special_saplings[item_key]
        result = compFactory.CreateItem(playerId).MayPlaceOn(itemName, auxValue, entityId_block_pos, Facing.Up)
        if not result and auxValue == 0:
            result = self.block_info_comp.MayPlace(itemName, entityId_block_pos, Facing.Up, dimensionId=dim)
        # print "plant", itemName, auxValue, "at", entityId_block_pos, result
        if result:
            item = self.item_comp.GetDroppedItem(entityId, getUserData=True)
            if item["count"] == 1:
                self.DestroyEntity(entityId)
                self.block_info_comp.SetBlockNew(entityId_block_pos, {"name": itemName, "aux": auxValue}, dimensionId=dim)
            else:
                item["count"] -= 1
                self.DestroyEntity(entityId)
                self.block_info_comp.SetBlockNew(entityId_block_pos, {"name": itemName, "aux": auxValue}, dimensionId=dim)
                self.CreateEngineItemEntity(item, dimensionId=dim, pos=item_entity_pos)

    def add_vein(self, playerId, affected_list):
        if affected_list:
            self.player_destroying[playerId].update(affected_list)
            player_block_info_comp = compFactory.CreateBlockInfo(playerId)
            for pos in affected_list[:-1]:
                player_block_info_comp.PlayerDestoryBlock(pos, 0, False)
            player_block_info_comp.PlayerDestoryBlock(affected_list[-1], 0, True)
            self.player_destroying[playerId].clear()

    @staticmethod
    def get_tree_type(state, fullName):
        if fullName == "minecraft:log":
            return state["old_log_type"]
        elif fullName == "minecraft:log2":
            return state["new_log_type"]
        return fullName

    @Listen.on("DestroyBlockEvent")
    def on_player_destroy_block(self, event):
        if not self.master_setting.tree_felling or self.master_setting.tree_felling_limit_count <= 0:
            return
        fullName = event["fullName"]
        if fullName not in self.master_setting.log_blocks:
            return
        pos = event["x"], event["y"], event["z"]
        playerId = event["playerId"]
        if pos in self.player_destroying[playerId]:
            self.player_destroying[playerId].discard(pos)
            return
        state = self.player_tree_falling_state.get(playerId, False)
        if not state:
            return
        handItem = compFactory.CreateItem(playerId).GetPlayerItem(ItemPosType.CARRIED)
        if not handItem or not isAxe(handItem["newItemName"], handItem["newAuxValue"]):
            return
        dimensionId = event["dimensionId"]
        oldBlockState = self.block_state_comp.GetBlockStatesFromAuxValue(fullName, event["auxData"])
        tree_type = self.get_tree_type(oldBlockState, fullName)

        searched = set()
        affected = []
        queue = [pos]
        found_one_with_leaves = not self.master_setting.check_leave_persistent_bit
        while queue:
            start_pos = queue.pop()
            for offset in BLOCKSURROUNDINGS:
                search_pos = start_pos[0] + offset[0], start_pos[1] + offset[1], start_pos[2] + offset[2]
                if search_pos in searched:
                    continue
                searched.add(search_pos)
                block = self.block_info_comp.GetBlockNew(search_pos, dimensionId)
                if not block:
                    continue
                if block["name"] == fullName:
                    state = self.block_state_comp.GetBlockStates(search_pos, dimensionId)
                    if not state or self.get_tree_type(state, block["name"]) == tree_type:
                        affected.append(search_pos)
                        queue.append(search_pos)
                        if len(affected) >= self.master_setting.tree_felling_limit_count:
                            if not found_one_with_leaves:
                                # 没有发现天然树叶
                                return
                            else:
                                self.add_vein(playerId, affected)
                                return
                elif not found_one_with_leaves and block["name"] in LEAVE_BLOCKS:
                    state = self.block_state_comp.GetBlockStates(search_pos, dimensionId)
                    if state and "persistent_bit" in state and not state["persistent_bit"]:
                        found_one_with_leaves = True
        if found_one_with_leaves:
            self.add_vein(playerId, affected)
