# -*- coding: utf-8 -*-
from .event import BaseEvent


class UnknowEvent(Exception):
    pass


class Listen:
    class CallableStr(str):
        def __call__(self, event_class, priority=0):
            return Listen.on(event_class, _type=self, priority=priority)

    server = CallableStr('server')
    minecraft = CallableStr('minecraft')
    mc = CallableStr('minecraft')
    client = CallableStr('client')

    @staticmethod
    def on(event_class, _type="minecraft", priority=0):
        if isinstance(event_class, basestring):
            event_name = event_class
        elif issubclass(event_class, BaseEvent):
            event_name = event_class.__name__
        else:
            raise UnknowEvent("unknown listening event")

        def decorator(func):
            func.listen_type = _type
            func.listen_event = event_name
            func.listen_priority = priority
            return func

        return decorator
