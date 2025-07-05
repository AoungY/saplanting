# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class ActorHurtServerEvent(BaseEvent):
    """触发时机：生物（包括玩家）受伤时触发

    - entityId : str 生物Id
    - cause : str 伤害来源，详见Minecraft枚举值文档的ActorDamageCause
    - damage : int 伤害值
    - absorbedDamage : int 吸收的伤害值（原始伤害减去damage）

    """
    pass


class ActuallyHurtServerEvent(BaseEvent):
    """实体实际受到伤害时触发，相比于DamageEvent，该伤害为经过护甲及buff计算后，实际的扣血量

    - srcId : str 伤害源id
    - projectileId : str 投射物id
    - entityId : str 被伤害id
    - damage : int 伤害值，允许修改，设置为0则此次造成的伤害为0
    - damage_f : float 伤害值（被伤害吸收后的值），允许修改，若修改该值，则会覆盖damage的修改效果
    - cause : str 伤害来源，详见Minecraft枚举值文档的ActorDamageCause

    """
    pass


class AddEffectServerEvent(BaseEvent):
    """触发时机：实体获得状态效果时

    - entityId : str 实体id
    - effectName : str 实体获得状态效果的名字
    - effectDuration : int 状态效果的持续时间，单位秒
    - effectAmplifier : int 状态效果的放大倍数
    - damage : int 状态造成的伤害值，如药水


    """
    pass


class ChangeSwimStateServerEvent(BaseEvent):
    """触发时机：实体开始或者结束游泳时

    - entityId : str 实体的唯一ID
    - formState : bool 事件触发前，实体是否在游泳状态
    - toState : bool 事件触发后，实体是否在游泳状态

    当实体的状态没有变化时，不会触发此事件，即formState和toState必定一真一假
    """

    pass


class DamageEvent(BaseEvent):
    """实体受到伤害时触发

    - srcId : str 伤害源id
    - projectileId : str 投射物id
    - entityId : str 被伤害id
    - damage : int 伤害值，允许修改，设置为0则此次造成的伤害为0
    - absorption : int 伤害吸收生命值，详见AttrType枚举的ABSORPTION
    - cause : str 伤害来源，详见Minecraft枚举值文档的ActorDamageCause
    - knock : bool 是否击退被攻击者，允许修改，设置该值为False则不产生击退
    - ignite : bool 是否点燃被伤害者，允许修改，设置该值为True产生点燃效果，反之亦然

    damage值会被护甲和absorption等吸收，不一定是最终扣血量。通过设置这个伤害值可以取消伤害，但不会取消由击退效果或者点燃效果带来的伤害

    当目标无法被击退时，knock值无效
    """
    pass


class EntityChangeDimensionServerEvent(BaseEvent):
    """实体维度改变时服务端抛出

    - entityId : str 实体id
    - fromDimensionId : int 维度改变前的维度
    - toDimensionId : int 维度改变后的维度
    - fromX : float 改变前的位置x
    - fromY : float 改变前的位置Y
    - fromZ : float 改变前的位置Z
    - toX : float 改变后的位置x
    - toY : float 改变后的位置Y
    - toZ : float 改变后的位置Z

    实体转移维度时，如果对应维度的对应位置的区块尚未加载，实体会缓存在维度自身的缓冲区中，直到对应区块被加载时才会创建对应的实体，此事件的抛出只代表实体从原维度消失，不代表必定会在对应维度出现
    """
    pass


class EntityDefinitionsEventServerEvent(BaseEvent):
    """触发时机：生物定义json文件中设置的event触发时同时触发。生物行为变更事件

    - entityId : str 生物id
    - eventName : str 触发的事件名称

    """
    pass


class EntityDieLoottableServerEvent(BaseEvent):
    """触发时机：生物死亡掉落物品时

    - dieEntityId : str 死亡实体的entityId
    - attacker : str 伤害来源的entityId
    - itemList : list(dict) 掉落物品列表，每个元素为一个itemDict，格式可参考物品信息字典
    - dirty : bool 默认为False，如果需要修改掉落列表需将该值设为True

    只有当dirty为True时才会重新读取item列表并生成对应的掉落物，如果不需要修改掉落结果的话请勿随意修改dirty值
    """
    pass


class EntityEffectDamageServerEvent(BaseEvent):
    """生物受到状态伤害/回复事件。

    - entityId : str 实体id
    - damage : int 伤害值（负数表示生命回复）
    - attributeBuffType : int 状态类型，参考AttributeBuffType
    - duration : float 状态持续时间，单位秒（s）
    - lifeTimer : float 状态生命时间，单位秒（s）
    - isInstantaneous : bool 是否为立即生效状态

    """

    pass


class EntityLoadScriptEvent(BaseEvent):
    """数据库加载实体自定义数据时触发

    - args : list 该事件的参数为长度为2的list，而非dict，其中list的第一个元素为实体id

    只有使用过extraData组件的实体才有此事件，触发时可以通过extraData组件获取该实体的自定义数据

    """

    pass


class EntityStartRidingEvent(BaseEvent):
    """当实体骑乘上另一个实体时触发

    - id : str 乘骑者实体id
    - rideId : str 被乘骑者实体id

    """
    pass


class EntityStopRidingEvent(BaseEvent):
    """触发时机：当实体停止骑乘时

    - id : str 实体id
    - rideId : str 坐骑id
    - exitFromRider : bool 是否下坐骑
    - entityIsBeingDestroyed : bool 坐骑是否将要销毁
    - switchingRides : bool 是否换乘坐骑
    - cancel : bool 设置为True可以取消（需要与客户端事件一同取消）

    以下情况不允许取消
        - ride组件StopEntityRiding接口
        - 玩家传送时
        - 坐骑死亡时
        - 玩家睡觉时
        - 玩家死亡时
        - 未驯服的马
        - 怕水的生物坐骑进入水里
        - 切换维度
    """
    pass


class EntityTickServerEvent(BaseEvent):
    """实体tick时触发。该事件为20帧每秒。需要使用AddEntityTickEventWhiteList添加触发该事件的实体类型白名单。

    - entityId : str 实体id
    - identifier : str 实体identifier
    """
    pass


class HealthChangeBeforeServerEvent(BaseEvent):
    """生物生命值发生变化之前触发

    - entityId : str	实体id
    - from : float	变化前的生命值
    - to : float	将要变化到的生命值，cancel设置为True时可以取消该变化，但是此参数不变
    - byScript : bool	是否通过SetAttrValue或SetAttrMaxValue调用产生的变化
    - cancel : bool	是否取消该变化
    """

    pass


class HealthChangeServerEvent(BaseEvent):
    """生物生命值发生变化时触发

    - entityId : str 实体id
    - from : float 变化前的生命值
    - to : float 变化后的生命值
    - byScript : bool 是否通过SetAttrValue或SetAttrMaxValue调用产生的变化

    """
    pass


class MobDieEvent(BaseEvent):
    """实体被玩家杀死时触发

    - id : str 实体id
    - attacker : str 伤害来源id

    注意：不能在该事件回调中对此玩家手持物品进行修改，如SpawnItemToPlayerCarried、ChangePlayerItemTipsAndExtraId等接口
    """
    pass


class MobGriefingBlockServerEvent(BaseEvent):
    """环境生物改变方块时触发，触发的时机与mobgriefing游戏规则影响的行为相同

    - cancel : bool 是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
    - blockX : int 方块x坐标
    - blockY : int 方块y坐标
    - blockZ : int 方块z坐标
    - entityId : str 触发的entity的唯一ID
    - blockName : str 方块的identifier，包含命名空间及名称
    - dimensionId : int 维度id

    触发的时机包括：生物踩踏耕地、破坏单个方块、破门、火矢点燃方块、凋灵boss破坏方块、末影龙破坏方块、末影人捡起方块、蠹虫破坏被虫蚀的方块、蠹虫把方块变成被虫蚀的方块、凋零杀死生物生成凋零玫瑰、生物踩坏海龟蛋。
    """

    pass


class OnFireHurtEvent(BaseEvent):
    """生物受到火焰伤害时触发

    - victim : str 受伤实体id
    - src : str 火焰创建者id
    - fireTime : float 着火时间，单位秒
    - cancel : bool 是否取消此处火焰伤害

    """
    pass

class OnGroundServerEvent(BaseEvent):
    """实体着地事件。实体，掉落的物品，点燃的TNT掉落地面时触发

    - id : str 实体id
    """
    pass


class OnKnockBackServerEvent(BaseEvent):
    """实体被击退时触发

    - id : str 实体id

    """
    pass


class ProjectileCritHitEvent(BaseEvent):
    """触发时机：当抛射物与头部碰撞时触发该事件。注：需调用OpenPlayerCritBox开启玩家爆头后才能触发。

    - id : str 子弹id
    - targetId : str 碰撞目标id

    """
    pass


class ProjectileDoHitEffectEvent(BaseEvent):
    """触发时机：当抛射物碰撞时触发该事件

    - id : str 子弹id
    - hitTargetType : str 碰撞目标类型,"ENTITY"或是"BLOCK"
    - targetId : str 碰撞目标id
    - hitFace : int 撞击在方块上的面id，参考Facing枚举
    - x : float 碰撞x坐标
    - y : float 碰撞y坐标
    - z : float 碰撞z坐标
    - blockPosX : int 碰撞是方块时，方块x坐标
    - blockPosY : int 碰撞是方块时，方块y坐标
    - blockPosZ : int 碰撞是方块时，方块z坐标
    - srcId : str 创建者id

    """
    pass


class RefreshEffectServerEvent(BaseEvent):
    """触发时机：实体身上状态效果更新时触发，更新条件1、新增状态等级较高，更新状态等级及时间；2、新增状态等级不变，时间较长，更新状态持续时间

    - entityId : str 实体id
    - effectName : str 更新状态效果的名字
    - effectDuration : int 更新后状态效果剩余持续时间，单位秒
    - effectAmplifier : int 更新后的状态效果放大倍数
    - damage : int 状态造成的伤害值，如药水

    """
    pass


class RemoveEffectServerEvent(BaseEvent):
    """触发时机：实体身上状态效果被移除时

    - entityId : str 实体id
    - effectName : str 被移除状态效果的名字
    - effectDuration : int 被移除状态效果的剩余持续时间，单位秒
    - effectAmplifier : int 被移除状态效果的放大倍数

    """
    pass


class SpawnProjectileServerEvent(BaseEvent):
    """触发时机：抛射物生成时触发

    - projectileId : str 抛射物的实体id
    - projectileIdentifier : str 抛射物的identifier
    - spawnerId : str 发射者的实体id，没有发射者时为-1


    """
    pass


class StartRidingServerEvent(BaseEvent):
    """触发时机：一个实体即将骑乘另外一个实体

    - cancel : bool 是否允许触发，默认为False，若设为True，可阻止触发后续的实体交互事件
    - actorId : str 骑乘者的唯一ID
    - victimId : str 被骑乘实体的唯一ID

    """
    pass


class WillAddEffectServerEvent(BaseEvent):
    """触发时机：实体即将获得状态效果前

    - entityId : str 实体id
    - effectName : str 实体获得状态效果的名字
    - effectDuration : int 状态效果的持续时间，单位秒
    - effectAmplifier : int 状态效果的放大倍数
    - cancel : bool 设置为True可以取消
    - damage : int 状态造成的伤害值，如药水；需要注意，该值不一定是最终的伤害值

    """
    pass


class WillTeleportToServerEvent(BaseEvent):
    """实体即将传送或切换维度

    - cancel : bool 是否允许触发，默认为False，若设为True，可阻止触发后续的传送
    - entityId : str 实体的唯一ID
    - fromDimensionId : int 传送前所在的维度
    - toDimensionId : int 传送后的目标维度
    - fromX : int 传送前所在的x坐标
    - fromY : int 传送前所在的y坐标
    - fromZ : int 传送前所在的z坐标
    - toX : int 传送目标地点的x坐标
    - toY : int 传送目标地点的y坐标
    - toZ : int 传送目标地点的z坐标
    - cause : str 传送理由，详情见MinecraftEnum.EntityTeleportCause

    假如目标维度尚未在内存中创建（即服务器启动之后，到传送之前，没有玩家进入过这个维度），那么此时事件中返回的目标地点坐标是算法生成的，不能保证正确。
    """
    pass
