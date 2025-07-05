# -*- coding: utf-8 -*-
from .event import BaseEvent


class UnknowEvent(Exception):
    """当监听一个未知事件时抛出的自定义异常。"""
    pass


class Listen:
    """
    事件监听装饰器的集合类。
    这个类本身不应被实例化，它主要作为访问装饰器的命名空间。
    例如：@Listen.on(), @Listen.server()
    """

    class CallableStr(str):
        """
        一个可调用字符串的内部类，这是实现 @Listen.server 这种语法的关键。
        它继承自str，但重写了__call__方法，使得类的实例（如'server'）可以像函数一样被调用。
        """
        def __call__(self, event_class, priority=0):
            """
            当实例被调用时，例如 @Listen.server("SomeEvent")，此方法会被执行。
            它实际上是一个快捷方式，最终会调用Listen.on这个主装饰器，
            并把实例自身（如'server'）作为事件类型（_type）传递过去。
            """
            return Listen.on(event_class, _type=self, priority=priority)

    # 创建CallableStr的实例，这样我们就可以使用 @Listen.server, @Listen.client 等语法
    server = CallableStr('server')
    minecraft = CallableStr('minecraft')
    mc = CallableStr('minecraft')  # mc是minecraft的别名
    client = CallableStr('client')

    @staticmethod
    def on(event_class, _type="minecraft", priority=0):
        """
        核心的事件监听装饰器工厂。
        它接收事件信息，并返回一个真正的装饰器。

        :param event_class: str或BaseEvent子类, 要监听的事件名称或事件类
        :param _type: str, 事件类型, 如 "minecraft", "server", "client"
        :param priority: int, 监听器的优先级
        """
        # 解析出事件的字符串名称
        if isinstance(event_class, basestring):
            event_name = event_class
        elif issubclass(event_class, BaseEvent):
            event_name = event_class.__name__
        else:
            raise UnknowEvent("unknown listening event")

        def decorator(func):
            """
            这是实际应用到目标方法上的装饰器。
            它的作用不是替换或包装原函数，而是给函数对象本身“贴上标签”，
            即添加几个自定义属性，用于存储事件监听所需的信息。
            后续的自动注册机制(onRegister)会读取这些属性来完成监听。
            """
            func.listen_type = _type
            func.listen_event = event_name
            func.listen_priority = priority
            return func

        return decorator
