# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class BlockLiquidStateChangeAfterServerEvent(BaseEvent):
    """
    触发时机：方块转为含水或者脱离含水(流体)后触发

    - blockName : str 方块的identifier，包含命名空间及名称
    - auxValue : int 方块附加值
    - dimension : int 方块维度
    - x : int 方块x坐标
    - y : int 方块y坐标
    - z : int 方块z坐标
    - turnLiquid : bool 是否转为含水，true则转为含水，false则脱离含水
    """
    blockName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxValue = None  # type: int
    """方块附加值"""
    dimension = None  # type: int
    """方块维度"""
    x = None  # type: int
    """方块x坐标"""
    y = None  # type: int
    """方块y坐标"""
    z = None  # type: int
    """方块z坐标"""
    turnLiquid = None  # type: bool
    """是否转为含水，true则转为含水，false则脱离含水"""


class BlockLiquidStateChangeServerEvent(BaseEvent):
    """
    触发时机：方块转为含水或者脱离含水(流体)前触发

    - blockName : str 方块的identifier，包含命名空间及名称
    - auxValue : int 方块附加值
    - dimension : int 方块维度
    - x : int 方块x坐标
    - y : int 方块y坐标
    - z : int 方块z坐标
    - turnLiquid : bool 是否转为含水，true则转为含水，false则脱离含水
    """
    blockName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxValue = None  # type: int
    """方块附加值"""
    dimension = None  # type: int
    """方块维度"""
    x = None  # type: int
    """方块x坐标"""
    y = None  # type: int
    """方块y坐标"""
    z = None  # type: int
    """方块z坐标"""
    turnLiquid = None  # type: bool
    """是否转为含水，true则转为含水，false则脱离含水"""


class BlockNeighborChangedServerEvent(BaseEvent):
    """
    触发时机：自定义方块周围的方块发生变化时，需要配置netease:neighborchanged_sendto_script，详情请查阅《自定义农作物》文档
    """

    dimensionId = None  # type: int
    """维度"""
    posX = None  # type: int
    """方块x坐标"""
    posY = None  # type: int
    """方块y坐标"""
    posZ = None  # type: int
    """方块z坐标"""
    blockName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxValue = None  # type: int
    """方块附加值"""
    neighborPosX = None  # type: int
    """变化方块x坐标"""
    neighborPosY = None  # type: int
    """变化方块y坐标"""
    neighborPosZ = None  # type: int
    """变化方块z坐标"""
    fromBlockName = None  # type: str
    """方块变化前的identifier，包含命名空间及名称"""
    fromBlockAuxValue = None  # type: int
    """方块变化前附加值"""
    toBlockName = None  # type: str
    """方块变化后的identifier，包含命名空间及名称"""
    toAuxValue = None  # type: int
    """方块变化后附加值"""


class BlockRandomTickServerEvent(BaseEvent):
    """
    触发时机：自定义方块配置netease:random_tick随机tick时
    """

    posX = None  # type: int
    """方块x坐标"""
    posY = None  # type: int
    """方块y坐标"""
    posZ = None  # type: int
    """方块z坐标"""
    blockName = None  # type: str
    """方块名称"""
    fullName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxValue = None  # type: int
    """方块附加值"""
    dimensionId = None  # type: int
    """实体维度"""


class BlockRemoveServerEvent(BaseEvent):
    """
    触发时机：监听该事件的方块在销毁时触发，可以通过ListenOnBlockRemoveEvent方法进行监听，或者通过json组件 netease:listen_block_remove 进行配置
    """
    x = None  # type: int
    """方块位置x"""
    y = None  # type: int
    """方块位置y"""
    z = None  # type: int
    """方块位置z"""
    fullName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxValue = None  # type: int
    """方块的附加值"""
    dimension = None  # type: int
    """该方块所在的维度"""


class BlockSnowStateChangeAfterServerEvent(BaseEvent):
    """
    触发时机：方块转为含雪或者脱离含雪后触发
    """
    dimension = None  # type: int
    """方块维度"""
    x = None  # type: int
    """方块x坐标"""
    y = None  # type: int
    """方块y坐标"""
    z = None  # type: int
    """方块z坐标"""
    turnSnow = None  # type: bool
    """是否转为含水，true则转为含雪，false则脱离含雪"""
    setBlockType = None  # type: int
    """方块进入脱离含雪的原因，参考SetBlockType"""


class BlockSnowStateChangeServerEvent(BaseEvent):
    """
    触发时机：方块转为含雪或者脱离含雪前触发
    """
    dimension = None  # type: int
    """方块维度"""
    x = None  # type: int
    """方块x坐标"""
    y = None  # type: int
    """方块y坐标"""
    z = None  # type: int
    """方块z坐标"""
    turnSnow = None  # type: bool
    """是否转为含水，true则转为含雪，false则脱离含雪"""
    setBlockType = None  # type: int
    """方块进入脱离含雪的原因，参考SetBlockType"""


class BlockStrengthChangedServerEvent(BaseEvent):
    """
    触发时机：自定义机械元件方块红石信号量发生变化时触发
    """

    posX = None  # type: int
    """方块x坐标"""
    posY = None  # type: int
    """方块y坐标"""
    posZ = None  # type: int
    """方块z坐标"""
    blockName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxValue = None  # type: int
    """方块附加值"""
    newStrength = None  # type: int
    """变化后的红石信号量"""
    dimensionId = None  # type: int
    """维度"""


class ChestBlockTryPairWithServerEvent(BaseEvent):
    """
    触发时机：两个并排的小箱子方块准备组合为一个大箱子方块时
    """
    cancel = None  # type: bool
    """是否允许触发，默认为False，若设为True，可阻止小箱子组合成为一个大箱子"""
    blockX = None  # type: int
    """小箱子方块x坐标"""
    blockY = None  # type: int
    """小箱子方块y坐标"""
    blockZ = None  # type: int
    """小箱子方块z坐标"""
    otherBlockX = None  # type: int
    """将要与之组合的另外一个小箱子方块x坐标"""
    otherBlockY = None  # type: int
    """将要与之组合的另外一个小箱子方块y坐标"""
    otherBlockZ = None  # type: int
    """将要与之组合的另外一个小箱子方块z坐标"""
    dimensionId = None  # type: int
    """维度id"""


class CommandBlockContainerOpenEvent(BaseEvent):
    """
    触发时机：玩家点击命令方块，尝试打开命令方块的设置界面
    """
    playerId = None  # type: str
    """玩家实体id"""
    isBlock = None  # type: bool
    """是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义"""
    blockX = None  # type: int
    """命令方块位置x，当isBlock为True时有效"""
    blockY = None  # type: int
    """命令方块位置y，当isBlock为True时有效"""
    blockZ = None  # type: int
    """命令方块位置z，当isBlock为True时有效"""
    victimId = None  # type: str
    """命令方块对应的逻辑实体的唯一id，当isBlock为False时有效"""
    cancel = None  # type: bool
    """修改为True时，可以阻止玩家打开命令方块的设置界面"""
    pass


class CommandBlockUpdateEvent(BaseEvent):
    """
    触发时机：玩家尝试修改命令方块的内置命令时

    当修改的目标为命令方块矿车时（此时isBlock为False），设置cancel为True，依旧可以阻止修改命令方块矿车的内部指令，但是从客户端能够看到命令方块矿车的内部指令变化了，不过这仅仅是假象，重新登录或者其他客户端打开命令方块矿车的设置界面，就会发现其实内部指令没有变化
    """

    playerId = None  # type: str
    """玩家实体id"""
    playerUid = None  # type: int
    """玩家的uid"""
    command = None  # type: str
    """企图修改的命令方块中的命令内容字符串"""
    isBlock = None  # type: bool
    """是否以方块坐标的形式定位命令方块，当为True时下述的blockX/blockY/blockZ有意义，当为False时，下述的victimId有意义"""
    blockX = None  # type: int
    """命令方块位置x，当isBlock为True时有效"""
    blockY = None  # type: int
    """命令方块位置y，当isBlock为True时有效"""
    blockZ = None  # type: int
    """命令方块位置z，当isBlock为True时有效"""
    victimId = None  # type: str
    """命令方块对应的逻辑实体的唯一id，当isBlock为False时有效"""
    cancel = None  # type: bool
    """修改为True时，可以阻止玩家修改命令方块的内置命令"""


class DestroyBlockEvent(BaseEvent):
    """
    触发时机：当方块已经被玩家破坏时触发该事件。

    在生存模式或创造模式下都会触发
    """

    x = None  # type: int
    """方块x坐标"""
    y = None  # type: int
    """方块y坐标"""
    z = None  # type: int
    """方块z坐标"""
    face = None  # type: int
    """方块被敲击的面向id，参考Facing枚举"""
    fullName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxData = None  # type: int
    """方块附加值"""
    playerId = None  # type: str
    """破坏方块的玩家ID"""
    dimensionId = None  # type: int
    """维度id"""


class EntityPlaceBlockAfterServerEvent(BaseEvent):
    """
    触发时机：当生物成功放置方块后触发

    部分放置后会产生实体的方块、可操作的方块、带有特殊逻辑的方块，不会触发该事件，包括但不限于床、门、告示牌、花盆、红石中继器、船、炼药锅、头部模型、蛋糕、酿造台、盔甲架等。
    """

    x = None  # type: int
    """方块x坐标"""
    y = None  # type: int
    """方块y坐标"""
    z = None  # type: int
    """方块z坐标"""
    fullName = None  # type: str
    """方块的identifier，包含命名空间及名称"""
    auxData = None  # type: int
    """方块附加值"""
    entityId = None  # type: str
    """试图放置方块的生物ID"""
    dimensionId = None  # type: int
    """维度id"""
    face = None  # type: int
    """点击方块的面，参考Facing枚举"""


class FallingBlockBreakServerEvent(BaseEvent):
    """
    触发时机：当下落的方块实体被破坏时，服务端触发该事件

    - fallingBlockId : str 下落的方块实体id
    - fallingBlockX : float 下落的方块实体位置x
    - fallingBlockY : float 下落的方块实体位置y
    - fallingBlockZ : float 下落的方块实体位置z
    - blockName : str 重力方块的identifier，包含命名空间及名称
    - fallTickAmount : int 下落的方块实体持续下落了多少tick
    - dimensionId : int 下落的方块实体维度id
    - cancelDrop : bool 是否取消方块物品掉落，可以在脚本层中设置

    不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义重力方块 ）
    """

    pass


class FallingBlockCauseDamageBeforeServerEvent(BaseEvent):
    """触发时机：当下落的方块开始计算砸到实体的伤害时，服务端触发该事件

    - fallingBlockId : str 下落的方块实体id
    - fallingBlockX : float 下落的方块实体位置x
    - fallingBlockY : float 下落的方块实体位置y
    - fallingBlockZ : float 下落的方块实体位置z
    - blockName : str 重力方块的identifier，包含命名空间及名称
    - dimensionId : int 下落的方块实体维度id
    - collidingEntitys : list(str) 当前碰撞到的实体列表id，如果没有的话是None
    - fallTickAmount : int 下落的方块实体持续下落了多少tick
    - fallDistance : float 下落的方块实体持续下落了多少距离
    - isHarmful : bool 是否计算对实体的伤害，引擎传来的值由json配置和伤害是否大于0决定，可在脚本层修改传回引擎
    - fallDamage : int 对实体的伤害，引擎传来的值距离和json配置决定，可在脚本层修改传回引擎

    不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义重力方块 ）

    服务端通常触发在客户端之后，而且有时会相差一个tick，这就意味着可能发生以下现象:服务端fallTickAmount比配置强制破坏时间多1tick，下落的距离、下落的伤害计算出来比客户端时间多1tick的误差。
    """

    pass


class FallingBlockReturnHeavyBlockServerEvent(BaseEvent):
    """触发时机：当下落的方块实体变回普通重力方块时，服务端触发该事件

    - fallingBlockId : int 下落的方块实体id
    - blockX : int 方块位置x
    - blockY : int 方块位置y
    - blockZ : int 方块位置z
    - heavyBlockName : str 重力方块的identifier，包含命名空间及名称
    - prevHereBlockName : str 变回重力方块时，原本方块位置的identifier，包含命名空间及名称
    - dimensionId : int 下落的方块实体维度id
    - fallTickAmount : int 下落的方块实体持续下落了多少tick

    不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义重力方块 ）
    """
    pass


class HeavyBlockStartFallingServerEvent(BaseEvent):
    """触发时机：当重力方块变为下落的方块实体后，服务端触发该事件

    - fallingBlockId : str 下落的方块实体id
    - blockX : int 方块位置x
    - blockY : int 方块位置y
    - blockZ : int 方块位置z
    - blockName : str 重力方块的identifier，包含命名空间及名称
    - dimensionId : int 下落的方块实体维度id

    不是所有下落的方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义重力方块 ）
    """

    pass


class HopperTryPullInServerEvent(BaseEvent):
    """触发时机：当漏斗上方连接容器后，容器往漏斗开始输入物品时触发，事件仅触发一次

    - x : int 漏斗位置x
    - y : int 漏斗位置y
    - z : int 漏斗位置z
    - abovePosX : int 交互的容器位置x
    - abovePosY : int 交互的容器位置y
    - abovePosZ : int 交互的容器位置z
    - dimensionId : int 维度id
    - canHopper : bool 是否允许容器往漏斗加东西(要关闭此交互，需先监听此事件再放置容器)

    """

    pass


class HopperTryPullOutServerEvent(BaseEvent):
    """触发时机：当漏斗以毗邻的方式连接容器时，即从旁边连接容器时，漏斗向容器开始输出物品时触发，事件仅触发一次

    - x : int 漏斗位置x
    - y : int 漏斗位置y
    - z : int 漏斗位置z
    - attachedPosX : int 交互的容器位置x
    - attachedPosY : int 交互的容器位置y
    - attachedPosZ : int 交互的容器位置z
    - dimensionId : int 维度id
    - canHopper : bool 是否允许漏斗往容器加东西(要关闭此交互，需先监听此事件再放置容器)

    """
    pass


class OnAfterFallOnBlockServerEvent(BaseEvent):
    """
    触发时机：当实体降落到方块后服务端触发，主要用于力的计算

    - entityId : str 实体id
    - posX : float 实体位置x
    - posY : float 实体位置y
    - posZ : float 实体位置z
    - motionX : float 瞬时移动X方向的力
    - motionY : float 瞬时移动Y方向的力
    - motionZ : float 瞬时移动Z方向的力
    - blockName : str 方块的identifier，包含命名空间及名称
    - calculate : bool 是否按脚本层传值计算力

    不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义方块JSON组件 ）

    如果要在脚本层修改motion，回传的需要是浮点型，例如需要赋值0.0而不是0

    如果需要修改实体的力，最好配合客户端事件同步修改，避免产生非预期现象

    因为引擎最后一定会按照原版方块规则计算力（普通方块置0，床、粘液块等反弹），所以脚本层如果想直接修改当前力需要将calculate设为true取消原版计算，按照传回值计算

    引擎在落地之后，OnAfterFallOnBlockServerEvent会一直触发，因此请在脚本层中做对应的逻辑判断

    """

    pass


class OnBeforeFallOnBlockServerEvent(BaseEvent):
    """触发时机：当实体刚降落到方块上时服务端触发，主要用于伤害计算

    - entityId : str 实体id
    - blockX : int 方块位置x
    - blockY : int 方块位置y
    - blockZ : int 方块位置z
    - blockName : str 方块的identifier，包含命名空间及名称
    - fallDistance : float 实体下降距离，可在脚本层传给引擎
    - cancel : bool 是否取消引擎对实体下降伤害的计算

    不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义方块JSON组件 ）

    如果要在脚本层修改fallDistance，回传的一定要是浮点型，例如需要赋值0.0而不是0

    可能会因为轻微的反弹触发多次，可在脚本层针对fallDistance的值进行判断
    """

    pass


class OnEntityInsideBlockServerEvent(BaseEvent):
    """触发时机：当实体碰撞盒所在区域有方块时，服务端持续触发

    - entityId : str 实体id
    - slowdownMultiX : float 实体移速X方向的减速比例，可在脚本层被修改
    - slowdownMultiY : float 实体移速Y方向的减速比例，可在脚本层被修改
    - slowdownMultiZ : float 实体移速Z方向的减速比例，可在脚本层被修改
    - blockX : int 方块位置x
    - blockY : int 方块位置y
    - blockZ : int 方块位置z
    - blockName : str 方块的identifier，包含命名空间及名称
    - cancel : bool 可由脚本层回传True给引擎，阻止触发后续原版逻辑

    不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义方块JSON组件 ） ，原版方块需要先通过RegisterOnEntityInside接口注册才能触发

    如果需要修改slowdownMulti/cancel，强烈建议与客户端事件同步修改，避免出现客户端表现不一致等非预期现象。

    如果要在脚本层修改slowdownMulti，回传的一定要是浮点型，例如需要赋值1.0而不是1

    有任意slowdownMulti参数被传回非0值时生效减速比例

    slowdownMulti参数更像是一个Buff，例如并不是立刻计算，而是先保存在实体属性里延后计算、在已经有slowdownMulti属性的情况下会取最低的值、免疫掉落伤害等，与原版蜘蛛网逻辑基本一致。

    """
    pass


class OnStandOnBlockServerEvent(BaseEvent):
    """触发时机：当实体站立到方块上时服务端持续触发

    - entityId : str 实体id
    - dimensionId : int 实体所在维度id
    - posX : float 实体位置x
    - posY : float 实体位置y
    - posZ : float 实体位置z
    - motionX : float 瞬时移动X方向的力
    - motionY : float 瞬时移动Y方向的力
    - motionZ : float 瞬时移动Z方向的力
    - blockX : int 方块位置x
    - blockY : int 方块位置y
    - blockZ : int 方块位置z
    - blockName : str 方块的identifier，包含命名空间及名称
    - cancel : bool 可由脚本层回传True给引擎，阻止触发后续原版逻辑

    不是所有方块都会触发该事件，需要在json中先配置触发开关（详情参考： 自定义方块JSON组件 ） ，原版方块需要先通过RegisterOnStandOn接口注册才能触发

    如果需要修改motion/cancel，强烈建议配合客户端事件同步修改，避免出现客户端表现不一致等现象

    如果要在脚本层修改motion，回传的一定要是浮点型，例如需要赋值0.0而不是0
    """

    pass


class PistonActionServerEvent(BaseEvent):
    """触发时机：活塞或者粘性活塞推送/缩回影响附近方块时

    - cancel : bool 是否允许触发，默认为False，若设为True，可阻止触发后续的事件
    - action : str 推送时=expanding；缩回时=retracting
    - pistonFacing : int 活塞的朝向，参考Facing枚举
    - pistonMoveFacing : int 活塞的运动方向，参考Facing枚举
    - dimensionId : int 活塞方块所在的维度
    - pistonX : int 活塞方块的x坐标
    - pistonY : int 活塞方块的y坐标
    - pistonZ : int 活塞方块的z坐标
    - blockList : list[(x,y,z),...] 活塞运动影响到产生被移动效果的方块坐标(x,y,z)，均为int类型
    - breakBlockList : list[(x,y,z),...] 活塞运动影响到产生被破坏效果的方块坐标(x,y,z)，均为int类型
    - entityList : list[string,...] 活塞运动影响到产生被移动或被破坏效果的实体的ID列表

    """

    pass


class ServerBlockEntityTickEvent(BaseEvent):
    """触发时机：自定义方块配置了netease:block_entity组件并设tick为true，玩家进入该方块的tick范围时触发

    - blockName : str 该方块名称
    - dimension : int 该方块所在的维度
    - posX : int 该方块的x坐标
    - posY : int 该方块的y坐标
    - posZ : int 该方块的z坐标

    """

    pass


class ServerBlockUseEvent(BaseEvent):
    """触发时机：玩家右键点击新版自定义方块（或者通过接口AddBlockItemListenForUseEvent增加监听的MC原生游戏方块）时服务端抛出该事件（该事件tick执行，需要注意效率问题）。

    - playerId : str 玩家Id
    - blockName : str 方块的identifier，包含命名空间及名称
    - aux : int 方块附加值
    - cancel : bool 设置为True可拦截与方块交互的逻辑。
    - x : int 方块x坐标
    - y : int 方块y坐标
    - z : int 方块z坐标
    - dimensionId : int 维度id

    """
    pass


class ServerEntityTryPlaceBlockEvent(BaseEvent):
    """
    触发时机：当生物试图放置方块时触发该事件。

    - x : int 方块x坐标
    - y : int 方块y坐标
    - z : int 方块z坐标
    - fullName : str 方块的identifier，包含命名空间及名称
    - auxData : int 方块附加值
    - entityId : str 试图放置方块的生物ID
    - dimensionId : int 维度id
    - face : int 点击方块的面，参考Facing枚举
    - cancel : bool 默认为False，在脚本层设置为True就能取消该方块的放置

    """
    pass


class ServerPlaceBlockEntityEvent(BaseEvent):
    """触发时机：手动放置或通过接口创建含自定义方块实体的方块时触发，此时可向该方块实体中存放数据

    - blockName : str 该方块名称
    - dimension : int 该方块所在的维度
    - posX : int 该方块的x坐标
    - posY : int 该方块的y坐标
    - posZ : int 该方块的z坐标
    """
    pass


class ServerPlayerTryDestroyBlockEvent(BaseEvent):
    """当玩家即将破坏方块时，服务端线程触发该事件。

    - x : int 方块x坐标
    - y : int 方块y坐标
    - z : int 方块z坐标
    - face : int 方块被敲击的面向id，参考Facing枚举
    - fullName : str 方块的identifier，包含命名空间及名称
    - auxData : int 方块附加值
    - playerId : str 试图破坏方块的玩家ID
    - dimensionId : int 维度id
    - cancel : bool 默认为False，在脚本层设置为True就能取消该方块的破坏
    - spawnResources : bool 是否生成掉落物，默认为True，在脚本层设置为False就能取消生成掉落物

    若需要禁止某些特殊方块的破坏，需要配合PlayerTryDestroyBlockClientEvent一起使用，例如床，旗帜，箱子这些根据方块实体数据进行渲染的方块
    """
    pass


class ShearsDestoryBlockBeforeServerEvent(BaseEvent):
    """触发时机：玩家手持剪刀破坏方块时，有剪刀特殊效果的方块会在服务端线程触发该事件

    - blockX : int 方块位置x
    - blockY : int 方块位置y
    - blockZ : int 方块位置z
    - blockName : str 方块的identifier，包含命名空间及名称
    - auxData : int 方块附加值
    - dropName : str 触发剪刀效果的掉落物identifier，包含命名空间及名称
    - dropCount : int 触发剪刀效果的掉落物数量
    - playerId : str 触发剪刀效果的玩家id
    - dimensionId : int 玩家触发时的维度id
    - cancelShears : bool 是否取消剪刀效果

    该事件触发在ServerPlayerTryDestroyBlockEvent之后，如果在ServerPlayerTryDestroyBlockEvent事件中设置了取消Destory或取消掉落物会导致该事件不触发

    取消剪刀效果后不掉落任何东西的方块类型：蜘蛛网、枯萎的灌木、草丛、下界苗、树叶、海草、藤蔓

    绊线取消剪刀效果需要配合ShearsDestoryBlockBeforeClientEvent同时使用，否则在表现上可能展现出来的还是剪刀剪断后的效果。绊线取消剪刀效果后依然会掉落成线。
    """

    pass


class StartDestroyBlockServerEvent(BaseEvent):
    """玩家开始挖方块时触发。创造模式下不触发。

    - pos : tuple(float,float,float) 方块的坐标
    - blockName : str 方块的identifier，包含命名空间及名称
    - auxValue : int 方块的附加值
    - playerId : str 玩家id
    - dimensionId : int 维度id
    - cancel : bool 修改为True时，可阻止玩家进入挖方块的状态。需要与StartDestroyBlockClientEvent一起修改。

    如果是隔着火焰挖方块，即使将该事件cancel掉，火焰也会被扑灭。如果要阻止火焰扑灭，需要配合ExtinguishFireServerEvent使用
    """

    pass


class StepOffBlockServerEvent(BaseEvent):
    """
    触发时机：实体移动离开一个实心方块时触发

    - blockX : int 方块x坐标
    - blockY : int 方块y坐标
    - blockZ : int 方块z坐标
    - entityId : str 触发的entity的唯一ID
    - blockName : str 方块的identifier，包含命名空间及名称
    - dimensionId : int 维度id

    不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： 自定义方块JSON组件 ）， 原版方块需要先通过RegisterOnStepOff接口注册才能触发
    """
    pass


class StepOnBlockServerEvent(BaseEvent):
    """触发时机：实体刚移动至一个新实心方块时触发。

    - cancel : bool 是否允许触发，默认为False，若设为True，可阻止触发后续物理交互事件
    - blockX : int 方块x坐标
    - blockY : int 方块y坐标
    - blockZ : int 方块z坐标
    - entityId : str 触发的entity的唯一ID
    - blockName : str 方块的identifier，包含命名空间及名称
    - dimensionId : int 维度id

    在合并微软更新之后，本事件触发时机与微软molang实验性玩法组件"minecraft:on_step_on"一致

    压力板与绊线钩在过去的版本的事件是可以触发的，但在更新后这种非实心方块并不会触发，有需要的可以使用OnEntityInsideBlockServerEvent事件。

    不是所有方块都会触发该事件，自定义方块需要在json中先配置触发开关（详情参考： 自定义方块JSON组件 ）， 原版方块需要先通过RegisterOnStepOn接口注册才能触发。原版的红石矿默认注册了，但深层红石矿没有默认注册。

    如果需要修改cancel，强烈建议配合客户端事件同步修改，避免出现客户端表现不一致等非预期现象。
    """
    pass
