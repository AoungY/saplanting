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
    """
    模组的服务端主System，负责处理所有服务端逻辑。
    包括自动种树、连锁砍树、配置管理和与客户端的通信。
    """

    def __init__(self, namespace, name):
        super(SaplantingServer, self).__init__(namespace, name)
        self.masterId = None  # 通常是第一个进入世界的玩家，拥有配置权限
        # 记录玩家连锁砍树的开关状态
        self.player_tree_falling_state = {}  # type: dict[str,bool]
        # 用于防止连锁砍树时重复触发破坏事件
        self.player_destroying = {}  # type: dict[str,set]
        # 初始化引擎组件
        self.game_comp = compFactory.CreateGame(self.levelId)
        self.item_comp = compFactory.CreateItem(self.levelId)
        self.msg_comp = compFactory.CreateMsg(self.levelId)
        self.block_info_comp = compFactory.CreateBlockInfo(self.levelId)
        self.block_state_comp = compFactory.CreateBlockState(self.levelId)
        # 加载服务端主配置
        self.master_setting = MasterSetting()
        self.master_setting.load()

    @Listen.on("OnCarriedNewItemChangedServerEvent")
    def on_player_hand_item_change(self, event):
        """
        监听玩家手持物品变化事件。
        如果玩家切换到斧头，则提示其连锁砍树的开关状态。
        """
        if not self.master_setting.tree_felling:
            return
        newItemDict = event["newItemDict"]
        if newItemDict and isAxe(newItemDict["newItemName"], newItemDict["newAuxValue"]):
            playerId = event["playerId"]
            state = self.player_tree_falling_state.get(playerId, False)
            self.game_comp.SetOneTipMessage(playerId, "连锁砍树:{}".format("§a开" if state else "§c关"))

    @Listen.client("SyncPlayerTreeFallingState")
    def on_sync_player_tree_falling_state(self, event):
        """监听客户端同步过来的连锁砍树开关状态"""
        playerId = event["__id__"] if "__id__" in event else event["playerId"]
        self.player_tree_falling_state[playerId] = event["state"]

    @Listen.on(ServerChatEvent)
    def on_command(self, event):
        """
        监听聊天事件，用于处理管理员指令。
        """
        playerId = event["playerId"]
        if playerId == self.masterId:  # 只有管理员能执行
            message = event["message"].lower()
            if message == "#hpldsg":  # 添加/移除自动种植白名单
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
            elif message == "#hpldsgmt":  # 添加/移除树木方块识别列表
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
        """
        监听客户端请求重载配置的事件。
        """
        self.master_setting.load()
        data = self.master_setting.get_client_data(add_saplings=False)
        self.BroadcastToAllClient("SyncMasterSetting", data)

    @Listen.on("LoadServerAddonScriptsAfter")
    def on_enabled(self, event=None):
        """
        服务端脚本加载完成事件，用于注册服务端配置项。
        """
        comp = serverApi.CreateComponent(self.levelId, "HeyPixel", "Config")
        if comp:
            from ..config.heyconfig_server import register_config_server
            comp.register_config(register_config_server)

    @Listen.on("ClientLoadAddonsFinishServerEvent")
    def on_player_login_finish(self, event):
        """
        客户端加载完成（即玩家进入游戏）事件。
        """
        playerId = event["playerId"]
        if self.masterId is None:  # 将第一个进入的玩家设为管理员
            self.masterId = playerId
        self.player_destroying[playerId] = set()
        # 将主配置同步给刚进入的玩家
        self.NotifyToClient(playerId, "SyncMasterSetting", self.master_setting.get_client_data())

    @Listen.on(DelServerPlayerEvent)
    def on_player_leave(self, event):
        """
        玩家离开游戏事件，用于清理玩家数据。
        """
        playerId = event["id"]
        if playerId in self.player_destroying:
            self.player_destroying.pop(playerId)

    @Listen.client("onSaplingOnGround")
    def on_sapling_on_ground(self, event):
        """
        监听客户端发来的树苗落地事件，执行种树逻辑。
        """
        playerId = event["__id__"] if "__id__" in event else event["playerId"]
        entityId = event["entityId"]
        if not self.game_comp.IsEntityAlive(entityId):
            return  # 实体可能已经被捡起或消失
        
        dim = compFactory.CreateDimension(entityId).GetEntityDimensionId()
        item_entity_pos = compFactory.CreatePos(entityId).GetFootPos()
        entityId_block_pos = get_block_pos(item_entity_pos)
        block = self.block_info_comp.GetBlockNew(entityId_block_pos, dimensionId=dim)
        
        if block:
            # 如果落在耕地上，则尝试在耕地上一格种植
            if block["name"] == "minecraft:farmland":
                entityId_block_pos = entityId_block_pos[0], entityId_block_pos[1] + 1, entityId_block_pos[2]
                block = self.block_info_comp.GetBlockNew(entityId_block_pos, dimensionId=dim)
                if not block:
                    return
            # 只能种植在空气或水中
            if block["name"] not in {"minecraft:air", "minecraft:water", "minecraft:flowing_water"}:
                return

        itemName = event["itemName"]
        auxValue = event["auxValue"]
        item_key = itemName, auxValue
        if item_key in special_saplings:  # 处理特殊树苗映射
            itemName, auxValue = special_saplings[item_key]
            
        # 检查是否可以放置
        result = compFactory.CreateItem(playerId).MayPlaceOn(itemName, auxValue, entityId_block_pos, Facing.Up)
        if not result and auxValue == 0:
            result = self.block_info_comp.MayPlace(itemName, entityId_block_pos, Facing.Up, dimensionId=dim)
        
        if result:
            item = self.item_comp.GetDroppedItem(entityId, getUserData=True)
            # 根据掉落物数量决定是消耗还是直接种植
            if item["count"] == 1:
                self.DestroyEntity(entityId)
                self.block_info_comp.SetBlockNew(entityId_block_pos, {"name": itemName, "aux": auxValue}, dimensionId=dim)
            else:
                item["count"] -= 1
                self.DestroyEntity(entityId)
                self.block_info_comp.SetBlockNew(entityId_block_pos, {"name": itemName, "aux": auxValue}, dimensionId=dim)
                self.CreateEngineItemEntity(item, dimensionId=dim, pos=item_entity_pos)

    def add_vein(self, playerId, affected_list):
        """
        执行连锁砍树的方块破坏。
        
        :param playerId: str, 玩家ID
        :param affected_list: list, 需要被破坏的方块坐标列表
        """
        if affected_list:
            self.player_destroying[playerId].update(affected_list)
            player_block_info_comp = compFactory.CreateBlockInfo(playerId)
            # 逐个破坏方块，最后一个方块才掉落物品，以模拟连锁效果
            for pos in affected_list[:-1]:
                player_block_info_comp.PlayerDestoryBlock(pos, 0, False)
            player_block_info_comp.PlayerDestoryBlock(affected_list[-1], 0, True)
            self.player_destroying[playerId].clear()

    @staticmethod
    def get_tree_type(state, fullName):
        """根据方块状态获取树木的具体类型（如oak, birch）"""
        if fullName == "minecraft:log":
            return state["old_log_type"]
        elif fullName == "minecraft:log2":
            return state["new_log_type"]
        return fullName

    @Listen.on("DestroyBlockEvent")
    def on_player_destroy_block(self, event):
        """
        监听玩家破坏方块事件，用于实现连锁砍树。
        """
        if not self.master_setting.tree_felling or self.master_setting.tree_felling_limit_count <= 0:
            return
        fullName = event["fullName"]
        if fullName not in self.master_setting.log_blocks:
            return  # 不是木头方块
        
        pos = event["x"], event["y"], event["z"]
        playerId = event["playerId"]
        
        # 如果这个方块是正在被连锁破坏的一部分，则忽略，防止无限循环
        if pos in self.player_destroying[playerId]:
            self.player_destroying[playerId].discard(pos)
            return
            
        # 检查玩家是否开启了连锁砍树
        state = self.player_tree_falling_state.get(playerId, False)
        if not state:
            return
            
        # 检查玩家是否手持斧头
        handItem = compFactory.CreateItem(playerId).GetPlayerItem(ItemPosType.CARRIED)
        if not handItem or not isAxe(handItem["newItemName"], handItem["newAuxValue"]):
            return
            
        dimensionId = event["dimensionId"]
        oldBlockState = self.block_state_comp.GetBlockStatesFromAuxValue(fullName, event["auxData"])
        tree_type = self.get_tree_type(oldBlockState, fullName)

        # 使用广度优先搜索（BFS）寻找所有相连的同种木头
        searched = set()
        affected = []
        queue = [pos]
        found_one_with_leaves = not self.master_setting.check_leave_persistent_bit
        
        while queue:
            start_pos = queue.pop()
            for offset in BLOCKSURROUNDINGS: # 遍历周围26个方块
                search_pos = start_pos[0] + offset[0], start_pos[1] + offset[1], start_pos[2] + offset[2]
                if search_pos in searched:
                    continue
                searched.add(search_pos)
                block = self.block_info_comp.GetBlockNew(search_pos, dimensionId)
                if not block:
                    continue
                
                # 如果是同种木头，加入待破坏列表
                if block["name"] == fullName:
                    state = self.block_state_comp.GetBlockStates(search_pos, dimensionId)
                    if not state or self.get_tree_type(state, block["name"]) == tree_type:
                        affected.append(search_pos)
                        queue.append(search_pos)
                        # 达到数量上限
                        if len(affected) >= self.master_setting.tree_felling_limit_count:
                            if not found_one_with_leaves:
                                return # 没有发现天然树叶，判定为人工建筑，不砍
                            else:
                                self.add_vein(playerId, affected)
                                return
                # 检查附近是否有天然树叶（persistent_bit为false），作为是“树”而非“建筑”的判断依据
                elif not found_one_with_leaves and block["name"] in LEAVE_BLOCKS:
                    state = self.block_state_comp.GetBlockStates(search_pos, dimensionId)
                    if state and "persistent_bit" in state and not state["persistent_bit"]:
                        found_one_with_leaves = True
                        
        if found_one_with_leaves:
            self.add_vein(playerId, affected)
