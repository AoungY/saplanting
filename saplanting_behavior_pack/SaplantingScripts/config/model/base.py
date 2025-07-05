# -*- coding: utf-8 -*-
# @Time    : 2023/7/24 11:13
# @Author  : taokyla
# @File    : base.py
class BaseConfig(object):

    def dump(self):
        return dict((k, v.dump() if isinstance(v, BaseConfig) else v) for k, v in self.__dict__.iteritems() if not k.startswith("_"))

    def load_data(self, data):
        for key in data:
            if hasattr(self, key):
                value = getattr(self, key)
                if isinstance(value, BaseConfig):
                    value.load_data(data[key])
                else:
                    setattr(self, key, data[key])

    def reset(self):
        for key in self.__dict__:
            if key in self.__class__.__dict__:
                self.__dict__[key] = self.__class__.__dict__[key]

    def get(self, key, default=None):
        if key in self.__dict__:
            return self.__dict__[key]
        return default

    def set(self, key, value):
        if key in self.__dict__:
            setattr(self, key, value)


class SavableConfig(BaseConfig):
    _KEY = "config_data_key"

    def load(self):
        raise NotImplementedError

    def update_config(self, config):
        self.load_data(config)
        self.save()

    def save(self):
        raise NotImplementedError