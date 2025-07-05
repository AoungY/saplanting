# -*- coding: utf-8 -*-

class BaseEvent(object):
    """
    所有自定义事件的基类。
    这个类本身是空的，其主要作用是作为一个标记，
    让事件系统可以通过 isinstance() 或 issubclass() 来识别自定义事件类。
    """
    pass