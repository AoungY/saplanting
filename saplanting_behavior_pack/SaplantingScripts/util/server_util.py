# -*- coding: utf-8 -*-
# @Time    : 2023/10/31 13:29
# @Author  : taokyla
# @File    : server_util.py
from copy import deepcopy

import mod.server.extraServerApi as serverApi
from mod.common.minecraftEnum import ItemPosType

compFactory = serverApi.GetEngineCompFactory()
itemComp = compFactory.CreateItem(serverApi.GetLevelId())

cachedItemInfos = {}


def GetItemInfo(itemName, auxValue, isEnchanted=False):
    key = (itemName, auxValue, isEnchanted)
    if key in cachedItemInfos:
        return cachedItemInfos[key]
    info = itemComp.GetItemBasicInfo(itemName, auxValue, isEnchanted=isEnchanted)
    cachedItemInfos[key] = info
    return info


axe_items_cache = {}


def isAxe(itemName, auxValue=0):
    if itemName in axe_items_cache:
        return axe_items_cache[itemName]
    info = GetItemInfo(itemName, auxValue)
    if info and info["itemType"] == "axe":
        axe_items_cache[itemName] = True
        return True
    axe_items_cache[itemName] = False
    return False

def is_same_itme_ignore_count(old, new):
    if old["newAuxValue"] == new["newAuxValue"] and old["newItemName"] == new["newItemName"]:
        old_userData = old["userData"] if "userData" in old else None
        new_userData = new["userData"] if "userData" in new else None
        return old_userData == new_userData
    else:
        return False


def AddItemToPlayerInventory(playerId, spawnitem):
    '''
    给玩家背包发放物品，优先发放到背包，背包已满时，生成物品实体到脚下
    :param playerId: 玩家id
    :param spawnitem: 物品itemdict，count可以大于60
    :return:
    '''
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
    if totalcanspawn < count:
        return False

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
