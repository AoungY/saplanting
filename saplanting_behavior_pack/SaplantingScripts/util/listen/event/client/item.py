# -*- coding: utf-8 -*-
from ..base_event import BaseEvent


class ActorAcquiredItemClientEvent(BaseEvent):
    """
    触发时机：玩家获得物品时客户端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点。）
    """
    actor = None  # type: str
    """获得物品玩家实体id"""
    secondaryActor = None  # type: str
    """物品给予者玩家实体id，如果不存在给予者的话，这里为空字符串"""
    itemDict = None  # type: dict
    """获取到的物品的物品信息字典"""
    acquireMethod = None  # type: int
    """获得物品的方法，详见ItemAcquisitionMethod"""


class ActorUseItemClientEvent(BaseEvent):
    """
    触发时机：玩家使用物品时客户端抛出的事件（比较特殊不走该事件的例子：1）喝牛奶；2）染料对有水的炼药锅使用；3）盔甲架装备盔甲）
    """
    playerId = None  # type: str
    """玩家实体id"""
    itemDict = None  # type: dict
    """使用的物品的物品信息字典"""
    useMethod = None  # type: int
    """使用物品的方法，详见ItemUseMethodEnum枚举"""


class AnvilCreateResultItemAfterClientEvent(BaseEvent):
    """
    玩家点击铁砧合成得到的物品时抛出的事件
    """
    playerId = None  # type: str
    """玩家实体id"""
    itemShowName = None  # type: str
    """合成后的物品显示名称"""
    itemDict = None  # type: dict
    """合成后的物品的物品信息字典"""
    oldItemDict = None  # type: dict
    """合成前的物品的物品信息字典（铁砧内第一个物品）"""
    materialItemDict = None  # type: dict
    """合成所使用材料的物品信息字典（铁砧内第二个物品）"""


class ClientItemTryUseEvent(BaseEvent):
    """
    玩家点击右键尝试使用物品时客户端抛出的事件，可以通过设置cancel为True取消使用物品。注：如果需要取消物品的使用需要同时在ClientItemTryUseEvent和ServerItemTryUseEvent中将cancel设置为True才能正确取消。

    ServerItemTryUseEvent/ClientItemTryUseEvent 不能取消对方块使用物品的行为，如使用生物蛋，使用桶倒出/收集，使用打火石点燃草等；如果想要取消这种行为，请使用ClientItemUseOnEvent和ServerItemUseOnEvent
    """
    playerId = None  # type: str
    """玩家id"""
    itemDict = None  # type: dict
    """使用的物品的物品信息字典"""
    cancel = None  # type: bool
    """取消使用物品"""


class ClientItemUseOnEvent(BaseEvent):
    """
    玩家在对方块使用物品时客户端抛出的事件。注：如果需要取消物品的使用需要同时在ClientItemUseOnEvent和ServerItemUseOnEvent中将ret设置为True才能正确取消。
    """
    entityId = None  # type: str
    """玩家实体id"""
    itemDict = None  # type: dict
    """使用的物品的物品信息字典"""
    x = None  # type: int
    """方块 x 坐标值"""
    y = None  # type: int
    """方块 y 坐标值"""
    z = None  # type: int
    """方块 z 坐标值"""
    blockName = None  # type: str
    """方块的identifier"""
    blockAuxValue = None  # type: int
    """方块的附加值"""
    face = None  # type: int
    """点击方块的面，参考Facing枚举"""
    clickX = None  # type: float
    """点击点的x比例位置"""
    clickY = None  # type: float
    """点击点的y比例位置"""
    clickZ = None  # type: float
    """点击点的z比例位置"""
    ret = None  # type: bool
    """设为True可取消物品的使用"""


class ClientShapedRecipeTriggeredEvent(BaseEvent):
    """
    玩家合成物品时触发
    """
    recipeId = None  # type: str
    """配方id，对应配方json文件中的identifier字段"""


class GrindStoneRemovedEnchantClientEvent(BaseEvent):
    """
    玩家点击砂轮合成得到的物品时抛出的事件
    """
    playerId = None  # type: str
    """玩家实体id"""
    oldItemDict = None  # type: dict
    """合成前的物品物品信息字典（砂轮内第一个物品）"""
    additionalItemDict = None  # type: dict
    """作为合成材料的物品物品信息字典（砂轮内第二个物品）"""
    newItemDict = None  # type: dict
    """合成后的物品物品信息字典"""
    exp = None  # type: int
    """本次合成返还的经验"""


class InventoryItemChangedClientEvent(BaseEvent):
    """
    玩家背包物品变化时客户端抛出的事件。

    如果槽位变空，变化后槽位中物品为空气

    触发时槽位物品仍为变化前物品

    背包内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序
    """
    playerId = None  # type: str
    """玩家实体id"""
    slot = None  # type: int
    """背包槽位"""
    oldItemDict = None  # type: dict
    """变化前槽位中的物品，格式参考物品信息字典"""
    newItemDict = None  # type: dict
    """变化后槽位中的物品，格式参考物品信息字典"""


class ItemReleaseUsingClientEvent(BaseEvent):
    """
    触发时机：释放正在使用的物品
    """
    playerId = None  # type: str
    """玩家id"""
    durationLeft = None  # type: float
    """蓄力剩余时间"""
    itemDict = None  # type: dict
    """使用的物品的物品信息字典"""
    maxUseDuration = None  # type: int
    """最大蓄力时长"""
    cancel = None  # type: bool
    """设置为True可以取消，需要同时取消服务端事件ItemReleaseUsingServerEvent"""


class OnCarriedNewItemChangedClientEvent(BaseEvent):
    """
    手持物品发生变化时，触发该事件；数量改变不会通知
    """
    itemDict = None  # type: dict
    """切换后物品的物品信息字典"""


class PlayerTryDropItemClientEvent(BaseEvent):
    """触发时机：玩家丢弃物品时触发
    """
    playerId = None  # type: str
    """玩家id"""
    itemDict = None  # type: dict
    """物品dict"""
    cancel = None  # type: bool
    """是否取消此次操作"""


class StartUsingItemClientEvent(BaseEvent):
    """
    玩家使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出
    """
    playerId = None  # type: str
    """玩家实体id"""
    itemDict = None  # type: dict
    """使用的物品的物品信息字典"""


class StopUsingItemClientEvent(BaseEvent):
    """
    玩家停止使用物品（目前仅支持Bucket、Trident、RangedWeapon、Medicine、Food、Potion、Crossbow、ChemistryStick）时抛出
    """
    playerId = None  # type: str
    """玩家实体id"""
    itemDict = None  # type: dict
    """使用的物品的物品信息字典"""