# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class ActorAcquiredItemServerEvent(BaseEvent):
    """触发时机：玩家获得物品时服务端抛出的事件（有些获取物品方式只会触发客户端事件，有些获取物品方式只会触发服务端事件，在使用时注意一点。）

    - actor : str 获得物品玩家实体id
    - secondaryActor : str 物品给予者玩家实体id，如果不存在给予者的话，这里为空字符串
    - itemDict : dict 获得的物品的物品信息字典
    - acquireMethod : int 获得物品的方法，详见ItemAcquisitionMethod枚举

    """
    pass


class ActorUseItemServerEvent(BaseEvent):
    """触发时机：玩家使用物品生效之前服务端抛出的事件（比较特殊不走该事件的例子：1）喝牛奶；2）染料对有水的炼药锅使用；3）盔甲架装备盔甲）

    - playerId : str 玩家实体id
    - itemDict : dict 使用的物品的物品信息字典
    - useMethod : int 使用物品的方法，详见ItemUseMethodEnum枚举

    """
    pass


class CraftItemOutputChangeServerEvent(BaseEvent):
    """玩家从容器拿出生成物品时触发

    - playerId : str 玩家实体id
    - itemDict : dict 生成的物品，格式参考物品信息字典
    - cancel : bool 是否取消生成物品

    支持合成台，铁砧，砂轮等工作方块

    通过cancel参数取消生成物品，可用于禁止外挂刷物品
    """
    pass


class ContainerItemChangedServerEvent(BaseEvent):
    """容器物品变化事件

    - pos             :	tuple(int,int,int)/None	容器坐标
    - containerType   :	int	容器类型，类型含义见：容器类型枚举
    - slot            :	int	容器槽位
    - oldItemDict     :  	dict	旧物品，格式参考物品信息字典
    - newItemDict     :	dict	新物品物品，格式参考物品信息字典

    """
    pass


class UIContainerItemChangedServerEvent(BaseEvent):
    """合成容器物品发生变化时触发

    - playerId      :	str	玩家实体id
    - slot          :	int	容器槽位，含义见：容器类型枚举
    - oldItemDict   :	dict	旧物品，格式参考物品信息字典
    - newItemDict   :	dict	生成的物品，格式参考物品信息字典
    """

    pass


class InventoryItemChangedServerEvent(BaseEvent):
    """玩家背包物品变化时服务端抛出的事件。

    - playerId : str 玩家实体id
    - slot : int 背包槽位
    - oldItemDict : dict 变化前槽位中的物品，格式参考物品信息字典
    - newItemDict : dict 变化后槽位中的物品，格式参考物品信息字典

    如果槽位变空，变化后槽位中物品为空气

    触发时槽位物品仍为变化前物品

    玩家进入游戏时，身上的物品会触发该事件

    背包内物品移动，合堆，分堆的操作会分多次事件触发并且顺序不定，编写逻辑时请勿依赖事件触发顺序
    """
    pass


class ItemReleaseUsingServerEvent(BaseEvent):
    """触发时机：释放正在使用的物品时

    - playerId : str 玩家id
    - durationLeft : float 蓄力剩余时间
    - itemDict : dict 使用的物品的物品信息字典
    - maxUseDuration : int 最大蓄力时长
    - cancel : bool 设置为True可以取消，需要同时取消客户端事件ItemReleaseUsingClientEvent

    """
    pass


class ItemUseAfterServerEvent(BaseEvent):
    """玩家在使用物品之后服务端抛出的事件。

    - entityId : str 玩家实体id
    - itemDict : dict 使用的物品的物品信息字典

    做出使用物品这个动作之后触发，一些需要蓄力的物品使用事件(ActorUseItemServerEvent)会在之后触发。如投掷三叉戟，先触发本事件，投出去之后再触发ActorUseItemServerEvent
    """
    pass


class ItemUseOnAfterServerEvent(BaseEvent):
    """玩家在对方块使用物品之后服务端抛出的事件

    - entityId : str 玩家实体id
    - itemDict : dict 使用的物品的物品信息字典
    - x : int 方块 x 坐标值
    - y : int 方块 y 坐标值
    - z : int 方块 z 坐标值
    - face : int 点击方块的面，参考Facing枚举
    - clickX : float 点击点的x比例位置
    - clickY : float 点击点的y比例位置
    - clickZ : float 点击点的z比例位置
    - blockName : str 方块的identifier
    - blockAuxValue : int 方块的附加值
    - dimensionId : int 维度id

    在ServerItemUseOnEvent和原版物品使用事件之后触发
    """
    pass


class OnCarriedNewItemChangedServerEvent(BaseEvent):
    """
    触发时机：玩家切换主手物品时触发该事件

    - oldItemDict : dict/None 旧物品的物品信息字典，当旧物品为空时，此项属性为None
    - newItemDict : dict/None 新物品的物品信息字典，当新物品为空时，此项属性为None
    - playerId : str 玩家 entityId

    切换耐久度不同的相同物品，不会触发该事件
    """
    pass


class OnItemPutInEnchantingModelServerEvent(BaseEvent):
    """触发时机：玩家将可附魔物品放到附魔台上时

    - playerId : str 玩家id，参数类型为str
    - slotType : int 玩家放入物品的EnchantSlotType
    - options : list 附魔台选项
    - change : bool 传入True时，附魔台选项会被新传入的options覆盖

    options为包含三个dict的list，单个dict的格式形如{"cost": 1, "enchantData": [(1,1)], "modEnchantData": [("custom_enchant, 1")]}，cost为解锁该选项所需的玩家等级，enchantData为该附魔选项包含的原版附魔数据，modEnchantData为该选项包含的自定义附魔数据
    """
    pass


class OnNewArmorExchangeServerEvent(BaseEvent):
    """触发时机：玩家切换盔甲时触发该事件

    - slot : int 槽位id
    - oldArmorDict : dict/None 旧装备的物品信息字典，当旧物品为空时，此项属性为None
    - newArmorDict : dict/None 新装备的物品信息字典，当新物品为空时，此项属性为None
    - playerId : str 玩家 entityId

    当玩家登录时，每个盔甲槽位会触发两次该事件，第一次为None切换到身上的装备，第二次的old和new都为身上装备。如果槽位为空，则是触发两次从None切换到None的事件。
    """
    pass


class OnOffhandItemChangedServerEvent(BaseEvent):
    """触发时机：玩家切换副手物品时触发该事件

    - oldItemDict : dict/None 旧物品的物品信息字典，当旧物品为空时，此项属性为None
    - newItemDict : dict/None 新物品的物品信息字典，当新物品为空时，此项属性为None
    - playerId : str 玩家 entityId

    """
    pass


class PlayerDropItemServerEvent(BaseEvent):
    """触发时机：玩家丢弃物品时触发

    - playerId : str 玩家id
    - itemEntityId : str 物品entityId
    """
    pass


class ServerItemTryUseEvent(BaseEvent):
    """玩家点击右键尝试使用物品时服务端抛出的事件。

    注：如果需要取消物品的使用需要同时在ClientItemTryUseEvent和ServerItemTryUseEvent中将cancel设置为True才能正确取消

    - playerId : str 玩家id
    - itemDict : dict 使用的物品的物品信息字典
    - cancel : bool 设为True可取消物品的使用

    ServerItemTryUseEvent/ClientItemTryUseEvent不能取消对方块使用物品的行为，如使用生物蛋，使用桶倒出/收集，使用打火石点燃草等；如果想要取消这种行为，请使用ClientItemUseOnEvent和ServerItemUseOnEvent
    """
    pass


class ServerItemUseOnEvent(BaseEvent):
    """玩家在对方块使用物品之前服务端抛出的事件。
    注：如果需要取消物品的使用需要同时在ClientItemUseOnEvent和ServerItemUseOnEvent中将ret设置为True才能正确取消。

    - entityId : str 玩家实体id
    - itemDict : dict 使用的物品的物品信息字典
    - x : int 方块 x 坐标值
    - y : int 方块 y 坐标值
    - z : int 方块 z 坐标值
    - blockName : str 方块的identifier
    - blockAuxValue : int 方块的附加值
    - face : int 点击方块的面，参考Facing枚举
    - dimensionId : int 维度id
    - clickX : float 点击点的x比例位置
    - clickY : float 点击点的y比例位置
    - clickZ : float 点击点的z比例位置
    - ret : bool 设为True可取消物品的使用

    当对原生方块进行使用时，如堆肥桶等类似有 使用 功能的方块使用物品时，不会触发该事件。而当原生方块加入监听后，ServerBlockUseEvent会触发。当需要获取触发时使用的物品时，可以通过item组件获取手中持有的物品，对应的客户端事件同理。
    """
    pass


class ServerPlayerTryTouchEvent(BaseEvent):
    """玩家即将捡起物品时触发

    - playerId : str 玩家Id
    - entityId : str 物品实体的Id
    - itemDict : dict 触碰的物品的物品信息字典
    - cancel : bool 设置为True时将取消本次拾取
    - pickupDelay : int 取消拾取后重新设置该物品的拾取cd，小于15帧将视作15帧，大于等于97813帧将视作无法拾取
    """
    pass


class ShearsUseToBlockBeforeServerEvent(BaseEvent):
    """触发时机：实体手持剪刀对方块使用时，有剪刀特殊效果的方块会在服务端线程触发该事件

    - blockX : int 方块位置x
    - blockY : int 方块位置y
    - blockZ : int 方块位置z
    - blockName : str 方块的identifier，包含命名空间及名称
    - auxData : int 方块附加值
    - dropName : str 触发剪刀效果的掉落物identifier，包含命名空间及名称
    - dropCount : int 触发剪刀效果的掉落物数量
    - entityId : str 触发剪刀效果的实体id，目前仅玩家会触发
    - dimensionId : int 玩家触发时的维度id
    - cancelShears : bool 是否取消剪刀效果

    目前会触发该事件的方块：南瓜、蜂巢

    该事件触发在ServerItemUseOnEvent之后，如果ServerItemUseOnEvent中取消了物品使用，该事件无法被触发

    和ServerItemUseOnEvent一样该事件判定在tick执行，意味着如果取消剪刀效果该事件可能会多次触发（取决于玩家按下使用键时长）
    """
    pass
