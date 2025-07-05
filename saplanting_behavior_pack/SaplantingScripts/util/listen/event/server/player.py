# -*- coding: utf-8 -*-
from ..base_event import BaseEvent


class MobDieEvent(BaseEvent):
    """实体被玩家杀死时触发

    - id : str 实体id
    - attacker : str 伤害来源id

    注意：不能在该事件回调中对此玩家手持物品进行修改，如SpawnItemToPlayerCarried、ChangePlayerItemTipsAndExtraId等接口
    """
    pass


class AddExpEvent(BaseEvent):
    """触发时机：当玩家增加经验时触发该事件。

    - id : str 玩家id
    - addExp : int 增加的经验值

    """
    pass


class AddLevelEvent(BaseEvent):
    """触发时机：当玩家升级时触发该事件。

    - id : str 玩家id
    - addLevel : int 增加的等级值
    - newLevel : int 新的等级

    """
    pass


class ChangeLevelUpCostServerEvent(BaseEvent):
    """触发时机：获取玩家下一个等级升级经验时，用于重载玩家的升级经验，每个等级在重置之前都只会触发一次

    - level : int 玩家当前等级
    - levelUpCostExp : int 当前等级升级到下个等级需要的经验值，当设置升级经验小于1时会被强制调整到1
    - changed : bool 设置为True，重载玩家升级经验才会生效

    """
    pass


class DimensionChangeFinishServerEvent(BaseEvent):
    """玩家维度改变完成后服务端抛出

    - playerId : str 玩家实体id
    - fromDimensionId : int 维度改变前的维度
    - toDimensionId : int 维度改变后的维度
    - toPos : tuple(float,float,float) 改变后的位置x,y,z,其中y值为脚底加上角色的身高值

    当通过传送门从末地回到主世界时，toPos的y值为32767，其他情况一般会比设置值高1.62
    """
    pass


class DimensionChangeServerEvent(BaseEvent):
    """玩家维度改变时服务端抛出

    - playerId : str 玩家实体id
    - fromDimensionId : int 维度改变前的维度
    - toDimensionId : int 维度改变后的维度
    - fromX : float 改变前的位置x
    - fromY : float 改变前的位置Y
    - fromZ : float 改变前的位置Z
    - toX : float 改变后的位置x
    - toY : float 改变后的位置Y
    - toZ : float 改变后的位置Z

    当通过传送门从末地回到主世界时，toY值为32767，其他情况一般会比设置值高1.62
    """
    pass


class ExtinguishFireServerEvent(BaseEvent):
    """玩家扑灭火焰时触发。下雨，倒水等方式熄灭火焰不会触发。

    - pos : tuple(float,float,float) 火焰方块的坐标
    - playerId : str 玩家id
    - cancel : bool 修改为True时，可阻止玩家扑灭火焰。需要与ExtinguishFireClientEvent一起修改。

    """

    pass


class GameTypeChangedServerEvent(BaseEvent):
    """个人游戏模式发生变化时服务端触发。

    - playerId : str 玩家Id，SetDefaultGameType接口改变游戏模式时该参数为空字符串
    - oldGameType : int 切换前的游戏模式
    - newGameType : int 切换后的游戏模式

    游戏模式：GetMinecraftEnum().GameType.*:Survival，Creative，Adventure分别为0~2 默认游戏模式发生变化时最后反映在个人游戏模式之上。
    """
    pass


class OnPlayerHitBlockServerEvent(BaseEvent):
    """触发时机：通过OpenPlayerHitBlockDetection打开方块碰撞检测后，当玩家碰撞到方块时触发该事件。监听玩家着地请使用客户端的OnGroundClientEvent。客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。

    - playerId : str 碰撞到方块的玩家Id
    - posX : int 碰撞方块x坐标
    - posY : int 碰撞方块y坐标
    - posZ : int 碰撞方块z坐标
    - blockId : str 碰撞方块的identifier
    - auxValue : int 碰撞方块的附加值
    - dimensionId : int 维度id

    """
    pass


class OnPlayerHitMobServerEvent(BaseEvent):
    """触发时机：通过OpenPlayerHitMobDetection打开生物碰撞检测后，当有生物与玩家碰撞时触发该事件。注：客户端和服务端分别作碰撞检测，可能两个事件返回的略有差异。

    - playerList : list[str] 生物碰撞到的玩家id的list

    """
    pass


class PlayerAttackEntityEvent(BaseEvent):
    """触发时机：当玩家攻击时触发该事件。

    - playerId : str 玩家id
    - victimId : str 受击者id
    - damage : int 伤害值：引擎传过来的值是0 允许脚本层修改为其他数
    - isValid : int 脚本是否设置伤害值：1表示是；0 表示否
    - cancel : bool 是否取消该次攻击，默认不取消
    - isKnockBack : bool 是否支持击退效果，默认支持，当不支持时将屏蔽武器击退附魔效果


    """
    pass


class PlayerCheatSpinAttackServerEvent(BaseEvent):
    """
    * 仅Apollo可用
    触发时机：玩家开始/结束快速旋转攻击并且不符合发送快速旋转攻击条件时触发（装备激流附魔的三叉戟、在水中或雨中，且未骑乘）

    - playerId : str 玩家的entityId
    - isStart : bool True时代表开始快速旋转攻击；False时代表结束快速旋转攻击

    假如没有自定义类似三叉戟/激流附魔的物品，那么触发此事件说明此有很大可能此玩家使用了【杀戮光环】外挂
    """
    pass


class PlayerDieEvent(BaseEvent):
    """触发时机：当玩家死亡时触发该事件。

    - id : str 玩家id
    - attacker : str 伤害来源id

    """
    pass


class PlayerDoInteractServerEvent(BaseEvent):
    """
    玩家与有minecraft:interact组件的生物交互时触发该事件，例如玩家手持空桶对牛挤奶、玩家手持打火石点燃苦力怕
    """
    playerId = None  # type: str
    itemDict = None  # type: dict
    interactEntityId = None  # type: str


class PlayerEatFoodServerEvent(BaseEvent):
    """触发时机：玩家吃下食物时触发

    - playerId : str 玩家Id
    - itemDict : dict 食物物品的物品信息字典
    - hunger : int 食物增加的饥饿值，可修改
    - nutrition : float 食物的营养价值，回复饱和度 = 食物增加的饥饿值 * 食物的营养价值 * 2，饱和度最大不超过当前饥饿值，可修改

    吃蛋糕以及喝牛奶不触发该事件
    """
    pass


class PlayerHurtEvent(BaseEvent):
    """触发时机：当玩家受伤害前触发该事件。

    - id : str 受击玩家id
    - attacker : str 伤害来源实体id，若没有实体攻击，例如高空坠落，id为-1

    """
    pass


class PlayerInteractServerEvent(BaseEvent):
    """触发时机：玩家即将和某个实体交互

    - cancel : bool 是否取消触发，默认为False，若设为True，可阻止触发后续的实体交互事件
    - playerId : str 主动与实体互动的玩家的唯一ID
    - itemDict : dict 当前玩家手持物品的物品信息字典
    - victimId : str 被动的实体的唯一ID

    """
    pass


class PlayerRespawnEvent(BaseEvent):
    """触发时机：玩家复活时触发该事件。

    - id : str 玩家id

    该事件为玩家点击重生按钮时触发，但是触发时玩家可能尚未完成复活，此时请勿对玩家进行切维度或设置生命值等操作 一般情况下推荐使用PlayerRespawnFinishServerEvent
    """
    pass


class PlayerRespawnFinishServerEvent(BaseEvent):
    """触发时机：玩家复活完毕时触发

    - id : str 玩家id

    该事件触发时玩家已重生完毕，可以安全使用切维度等操作
    """
    pass


class PlayerSleepServerEvent(BaseEvent):
    """玩家使用床睡觉成功

    - playerId : str 玩家id

    """
    pass


class PlayerSpinAttackServerEvent(BaseEvent):
    """* 仅Apollo可用
    触发时机：玩家开始/结束快速旋转攻击时触发

    - playerId : str 玩家的entityId
    - isInWaterOrRain : bool 是否在水中或雨中
    - isRiding : bool 是否骑乘状态
    - isStart : bool True时代表开始快速旋转攻击；False时代表结束快速旋转攻击

    """
    pass


class PlayerStopSleepServerEvent(BaseEvent):
    """玩家停止睡觉

    - playerId : str 玩家id
    """
    pass


class PlayerTeleportEvent(BaseEvent):
    """触发时机：当玩家传送时触发该事件，如：玩家使用末影珍珠或tp指令时。

    - id : str 玩家id

    """
    pass


class PlayerTrySleepServerEvent(BaseEvent):
    """玩家尝试使用床睡觉

    - playerId : str 玩家id
    - cancel : bool 是否取消（开发者传入）

    """
    pass


class ServerPlayerGetExperienceOrbEvent(BaseEvent):
    """触发时机：玩家获取经验球时触发的事件

    - playerId : str 玩家id
    - experienceValue : int 经验球经验值
    - cancel : bool 是否取消（开发者传入）

    cancel值设为True时，捡起的经验球不会增加经验值，但是经验球一样会消失。
    """
    pass


class StoreBuySuccServerEvent(BaseEvent):
    """触发时机:玩家游戏内购买商品时服务端抛出的事件

    - playerId : str 购买商品的玩家实体id

    """
    pass


class lobbyGoodBuySucServerEvent(BaseEvent):
    """触发时机:玩家联机大厅登录或者联机大厅游戏内购买商品时服务端抛出的事件

    - playerId : str 购买商品的玩家实体id
    - uid : str 购买商品的玩家uid
    - resid : int 当前游戏id

    """
    pass
