# -*- coding: utf-8 -*-
# @Time    : 2023/10/31 13:29
# @Author  : taokyla
# @File    : server_util.py
from copy import deepcopy

import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import ItemPosType

compFactory = serverApi.GetEngineCompFactory()
itemComp = compFactory.CreateItem(serverApi.GetLevelId())

# 缓存物品信息，避免重复调用API
cachedItemInfos = {}


def GetItemInfo(itemName, auxValue, isEnchanted=False):
    """
    获取物品的基本信息，并使用缓存来优化性能。
    :param itemName: str, 物品ID
    :param auxValue: int, 物品附加值
    :param isEnchanted: bool, 是否为附魔书
    :return: dict, 物品信息字典
    """
    key = (itemName, auxValue, isEnchanted)
    if key in cachedItemInfos:
        return cachedItemInfos[key]
    info = itemComp.GetItemBasicInfo(itemName, auxValue, isEnchanted=isEnchanted)
    cachedItemInfos[key] = info
    return info


# 缓存斧头类物品的判断结果
axe_items_cache = {}


def isAxe(itemName, auxValue=0):
    """
    判断一个物品是否为“斧头”。
    同样使用了缓存来优化性能。
    """
    if itemName in axe_items_cache:
        return axe_items_cache[itemName]
    info = GetItemInfo(itemName, auxValue)
    if info and info["itemType"] == "axe":
        axe_items_cache[itemName] = True
        return True
    axe_items_cache[itemName] = False
    return False

def is_same_itme_ignore_count(old, new):
    """
    比较两个物品字典，判断它们是否为同一种物品（忽略数量）。
    除了比较ID和附加值，还会比较userData，以区分NBT不同的物品。
    """
    if old["newAuxValue"] == new["newAuxValue"] and old["newItemName"] == new["newItemName"]:
        old_userData = old["userData"] if "userData" in old else None
        new_userData = new["userData"] if "userData" in new else None
        return old_userData == new_userData
    else:
        return False


def AddItemToPlayerInventory(playerId, spawnitem):
    """
    向玩家背包中添加物品，提供比引擎原生接口更完善的功能。
    它会自动处理堆叠、填充空位；如果背包已满，会自动将物品生成在玩家脚下。
    :param playerId: str, 玩家ID
    :param spawnitem: dict, 物品字典，数量(count)可以超过最大堆叠数
    :return: bool, 恒为True
    """
    itemName = spawnitem["newItemName"]
    auxValue = spawnitem["newAuxValue"]
    count = spawnitem['count'] if 'count' in spawnitem else 0
    if count <= 0:
        return True
    info = itemComp.GetItemBasicInfo(itemName, auxValue)
    if info:
        maxStackSize = info['maxStackSize']
    else:
        maxStackSize = 1

    itemcomp = compFactory.CreateItem(playerId)
    playerInv = itemcomp.GetPlayerAllItems(ItemPosType.INVENTORY, True)

    # 优先尝试堆叠到已有物品或空槽位
    for slotId, itemDict in enumerate(playerInv):
        if count > 0:
            if itemDict:
                if is_same_itme_ignore_count(itemDict, spawnitem):
                    canspawncount = maxStackSize - itemDict['count']
                    spawncount = min(canspawncount, count)
                    num = spawncount + itemDict['count']
                    itemcomp.SetInvItemNum(slotId, num)
                    count -= spawncount
            else:
                spawncount = min(maxStackSize, count)
                itemDict = deepcopy(spawnitem)
                itemDict['count'] = spawncount
                itemcomp.SpawnItemToPlayerInv(itemDict, playerId, slotId)
                count -= spawncount
        else:
            return True
    # 如果背包已满，则在玩家位置生成掉落物
    while count > 0:
        spawncount = min(maxStackSize, count)
        itemDict = deepcopy(spawnitem)
        itemDict['count'] = spawncount
        dim = compFactory.CreateDimension(playerId).GetEntityDimensionId()
        pos = compFactory.CreatePos(playerId).GetPos()
        pos = (pos[0], pos[1] - 1, pos[2])
        itemComp.SpawnItemToLevel(itemDict, dim, pos)
        count -= spawncount
    return True


def AddItemToContainer(chestpos, spawnitem, dimension=0):
    """
    向容器（如箱子）中添加物品。
    此函数会先检查容器是否有足够空间，只有空间足够时才会执行添加操作。
    :param chestpos: tuple, 容器的坐标(x, y, z)
    :param spawnitem: dict, 要添加的物品字典
    :param dimension: int, 容器所在的维度ID
    :return: bool, 如果成功添加返回True，如果空间不足则返回False
    """
    size = itemComp.GetContainerSize(chestpos, dimension)
    if size < 0:
        return False
    itemName = spawnitem["newItemName"]
    auxValue = spawnitem["newAuxValue"]
    count = spawnitem['count'] if 'count' in spawnitem else 0
    if count <= 0:
        return True
    info = itemComp.GetItemBasicInfo(itemName, auxValue)
    if info:
        maxStackSize = info['maxStackSize']
    else:
        maxStackSize = 1

    # 第一步：计算容器内总共还能放下多少目标物品
    totalcanspawn = 0
    canspawnslotlist = []
    for slotId in range(size):
        if totalcanspawn < count:
            itemDict = itemComp.GetContainerItem(chestpos, slotId, dimension, getUserData=True)
            if itemDict:
                if is_same_itme_ignore_count(itemDict, spawnitem):
                    canspawncount = maxStackSize - itemDict['count']
                    if canspawncount > 0:
                        totalcanspawn += canspawncount
                        canspawnslotlist.append([slotId, canspawncount])
            else:
                totalcanspawn += maxStackSize
                canspawnslotlist.append([slotId, maxStackSize])
        else:
            break
    # 如果总空间不足，直接返回失败
    if totalcanspawn < count:
        return False

    # 第二步：如果空间足够，则执行添加操作
    spawnResult = False
    for slotId, canspawncount in canspawnslotlist:
        if count > 0:
            itemDict = itemComp.GetContainerItem(chestpos, slotId, dimension, getUserData=True)
            if not itemDict:
                itemDict = deepcopy(spawnitem)
                itemDict['count'] = 0
            spawncount = min(canspawncount, count)
            itemDict['count'] = spawncount + itemDict['count']
            r = itemComp.SpawnItemToContainer(itemDict, slotId, chestpos, dimension)
            if r:
                spawnResult = True
            count -= spawncount
        else:
            break
    return spawnResult
