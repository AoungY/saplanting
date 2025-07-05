# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class ClientJumpButtonPressDownEvent(BaseEvent):
    """
    跳跃按钮按下事件，返回值设置参数只对当次按下事件起作用
    """
    continueJump = None  # type: bool
    """设置是否执行跳跃逻辑"""


class ClientJumpButtonReleaseEvent(BaseEvent):
    """跳跃按钮按下释放事件"""
    pass


class GetEntityByCoordEvent(BaseEvent):
    """
    玩家点击屏幕时触发，多个手指点在屏幕上时，只有第一个会触发。
    """
    pass


class GetEntityByCoordReleaseClientEvent(BaseEvent):
    """玩家点击屏幕后松开时触发，多个手指点在屏幕上时，只有最后一个手指松开时触发。"""
    pass


class HoldBeforeClientEvent(BaseEvent):
    """玩家长按屏幕，即将响应到游戏内时触发。仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用RightClickBeforeClientEvent事件监听鼠标右键

    玩家长按屏幕的处理顺序为：
        - 玩家点击屏幕，在长按判定时间内（默认为400毫秒，可通过SetHoldTimeThreshold接口修改）一直没有进行拖动或松手
        - 触发该事件
        - 若事件没有cancel，则根据主手上的物品，准心处的物体类型以及与玩家的距离，进行挖方块/使用物品/与实体交互等操作 即该事件只会在到达长按判定时间的瞬间触发一次，后面一直按住不会连续触发，可以使用TapOrHoldReleaseClientEvent监听长按后松手

    与TapBeforeClientEvent事件类似，被ui层捕获，没有穿透到世界的点击不会触发该事件
    """
    cancel = None  # type: bool
    """设置为True可拦截原版的挖方块/使用物品/与实体交互响应"""


class LeftClickBeforeClientEvent(BaseEvent):
    """
    玩家按下鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。
    """
    cancel = None  # type: bool
    """设置为True可拦截原版的挖方块或攻击响应"""


class LeftClickReleaseClientEvent(BaseEvent):
    """玩家松开鼠标左键时触发。仅在pc的普通控制模式（即非F11模式）下触发。"""
    pass


class OnBackButtonReleaseClientEvent(BaseEvent):
    """返回按钮（目前特指安卓系统导航中的返回按钮）松开时触发"""
    pass


class OnClientPlayerStartMove(BaseEvent):
    """移动按钮按下触发事件，在按住一个方向键的同时，去按另外一个方向键，不会触发第二次"""
    pass


class OnClientPlayerStopMove(BaseEvent):
    """移动按钮按下释放时触发事件，同时按下多个方向键，需要释放所有的方向键才会触发事件"""
    pass


class OnKeyPressInGame(BaseEvent):
    """
    按键按下或按键释放时触发
    """
    screenName = None  # type: str
    """当前screenName"""
    key = None  # type: str
    """键码（注：这里的int型被转成了str型，比如"1"对应的就是枚举值文档中的1），详见KeyBoardType枚举"""
    isDown = None  # type: str
    """是否按下，按下为1，弹起为0"""


class RightClickBeforeClientEvent(BaseEvent):
    """
    玩家按下鼠标右键时触发。仅在pc下触发（普通控制模式及F11模式都会触发）。
    """

    cancel = None  # type: bool
    """设置为True可拦截原版的物品使用/实体交互响应"""


class RightClickReleaseClientEvent(BaseEvent):
    """玩家松开鼠标右键时触发。仅在pc的普通控制模式（即非F11模式）下触发。在F11下右键，按下会触发RightClickBeforeClientEvent，松开时会触发TapOrHoldReleaseClientEvent"""
    pass


class TapBeforeClientEvent(BaseEvent):
    """玩家点击屏幕并松手，即将响应到游戏内时触发。仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用LeftClickBeforeClientEvent事件监听鼠标左键

    玩家点击屏幕的处理顺序为：
        - 玩家点击屏幕，没有进行拖动，并在短按判定时间（250毫秒）内松手
        - 触发该事件
        - 若事件没有cancel，则根据准心处的物体类型以及与玩家的距离，进行攻击或放置等操作

    与GetEntityByCoordEvent事件不同的是，被ui层捕获，没有穿透到世界的点击不会触发该事件，例如：
        - 点击原版的移动/跳跃等按钮，
        - 通过SetIsHud(0)屏蔽了游戏操作
        - 对按钮使用AddTouchEventHandler接口时isSwallow参数设置为True
    """
    cancel = None  # type: bool
    """设置为True可拦截原版的攻击或放置响应"""


class TapOrHoldReleaseClientEvent(BaseEvent):
    """玩家点击屏幕后松手时触发。仅在移动端或pc的F11模式下触发。pc的非F11模式可以使用LeftClickReleaseClientEvent与RightClickReleaseClientEvent事件监听鼠标松开"""
    pass