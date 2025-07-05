# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:13
# @Author  : taokyla
# @File    : base.py
class BaseConfig(object):
    """
    配置模型的基类，提供了配置数据与字典之间相互转换的基础功能。
    """

    def dump(self):
        """
        将配置实例序列化为一个字典。
        该方法会遍历实例的所有属性，并把不以下划线"_"开头的属性转换成字典的键值对。
        如果属性值本身也是一个BaseConfig实例，会递归调用其dump方法，从而支持嵌套配置。
        :return: dict, 包含了配置数据的字典
        """
        return dict((k, v.dump() if isinstance(v, BaseConfig) else v) for k, v in self.__dict__.iteritems() if not k.startswith("_"))

    def load_data(self, data):
        """
        从字典加载数据来更新配置实例。
        该方法会遍历字典的键，并更新实例中对应的属性值。
        同样支持嵌套的BaseConfig。
        :param data: dict, 包含配置数据的字典
        """
        for key in data:
            if hasattr(self, key):
                value = getattr(self, key)
                if isinstance(value, BaseConfig):
                    value.load_data(data[key])
                else:
                    setattr(self, key, data[key])

    def reset(self):
        """
        将实例的配置重置为类中定义的默认值。
        它通过比较实例属性和类属性来实现。
        """
        for key in self.__dict__:
            if key in self.__class__.__dict__:
                self.__dict__[key] = self.__class__.__dict__[key]

    def get(self, key, default=None):
        """
        安全地获取一个配置项的值。
        :param key: str, 配置项的键
        :param default: any, 如果键不存在时返回的默认值
        :return: any, 配置项的值
        """
        if key in self.__dict__:
            return self.__dict__[key]
        return default

    def set(self, key, value):
        """
        安全地设置一个配置项的值。
        :param key: str, 配置项的键
        :param value: any, 要设置的值
        """
        if key in self.__dict__:
            setattr(self, key, value)


class SavableConfig(BaseConfig):
    """
    可持久化配置的基类，继承自BaseConfig。
    增加了加载(load)和保存(save)的抽象接口，要求子类必须实现具体的持久化逻辑。
    """
    _KEY = "config_data_key"
    """配置的唯一标识符，通常用作文件名或数据库键。"""

    def load(self):
        """
        从持久化存储（如文件）中加载配置。
        这是一个抽象方法，子类必须重写它。
        """
        raise NotImplementedError

    def update_config(self, config):
        """
        使用给定的字典更新配置，并立即保存。
        :param config: dict, 新的配置数据
        """
        self.load_data(config)
        self.save()

    def save(self):
        """
        将当前配置保存到持久化存储（如文件）中。
        这是一个抽象方法，子类必须重写它。
        """
        raise NotImplementedError