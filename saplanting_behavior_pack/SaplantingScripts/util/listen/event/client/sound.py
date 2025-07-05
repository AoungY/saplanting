# -*- coding: utf-8 -*-
from ..base_event import BaseEvent

class OnMusicStopClientEvent(BaseEvent):
    """
    音乐停止时，当玩家调用StopCustomMusic来停止自定义背景音乐时，会触发该事件
    """
    musicName = None  # type: str
    """音乐名称"""


class PlayMusicClientEvent(BaseEvent):
    """
    播放背景音乐时触发
    """
    name = None  # type: str
    """即资源包中sounds/music_definitions.json中的event_name，并且对应sounds/sound_definitions.json中的key"""
    cancel = None  # type: bool
    """设为True可屏蔽该次音效播放"""
    pass


class PlaySoundClientEvent(BaseEvent):
    """
    播放场景音效或UI音效时触发
    """
    name = None  # type: str
    """即资源包中sounds/sound_definitions.json中的key"""
    pos = None  # type: tuple[float,float,float]
    """播放的位置。UI音效为(0,0,0)"""
    volume = None  # type: float
    """音量，范围为0-1"""
    pitch = None  # type: float
    """播放速度，正常速度为1"""
    cancel = None  # type: bool
    """设为True可屏蔽该次音效播放"""