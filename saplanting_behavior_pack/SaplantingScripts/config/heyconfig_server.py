# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 9:41
# @Author  : taokyla
# @File    : heyconfig_server.py
from .modConfig import MASTER_SETTING_CONFIG_NAME, ModName, ClientSystemName
from .model.server import ServerSavableConfig
from .sapling import default_saplings, LOG_BLOCKS


class MasterSetting(ServerSavableConfig):
    _KEY = MASTER_SETTING_CONFIG_NAME

    saplings = default_saplings
    min_wait_time = 3
    tree_felling = True
    check_leave_persistent_bit = True
    tree_felling_limit_count = 255
    log_blocks = LOG_BLOCKS

    def __init__(self):
        self.saplings = default_saplings  # type: set[tuple[str, int]]
        self.min_wait_time = 3
        self.tree_felling = True
        self.check_leave_persistent_bit = True
        self.tree_felling_limit_count = 255
        self.log_blocks = LOG_BLOCKS

    def load_data(self, data):
        if "min_wait_time" in data:
            data["min_wait_time"] = max(0, data["min_wait_time"])
        if "saplings" in data:
            data["saplings"] = set(tuple(value) for value in data["saplings"])
        if "log_blocks" in data:
            data["log_blocks"] = set(data["log_blocks"])
        super(MasterSetting, self).load_data(data)

    def dump(self):
        data = super(MasterSetting, self).dump()
        if "saplings" in data:
            data["saplings"] = list(list(value) for value in data["saplings"])
        if "log_blocks" in data:
            data["log_blocks"] = list(data["log_blocks"])
        return data

    def get_client_data(self, add_min_wait_time=True, add_saplings=True):
        data = {}
        if add_min_wait_time:
            data["min_wait_time"] = self.min_wait_time
        if add_saplings:
            data["saplings"] = list(list(value) for value in self.saplings)
        return data


register_config_server = {
    "name": "落地生根",
    "mod": ModName,
    "permission": "host",
    "categories": [

        {
            "name": "房主设置",
            "key": MASTER_SETTING_CONFIG_NAME,
            "title": "落地生根房主设置",
            "icon": "textures/ui/op",
            "permission": "host",
            "global": True,
            "callback": {
                "function": "CALLBACK",
                "extra": {
                    "name": ModName,
                    "system": ClientSystemName,
                    "function": "reload_master_setting"
                }
            },
            "items": [
                {
                    "type": "label",
                    "size": 0.9,
                    "name": "房主手持物品，聊天栏输入\"§l§a#hpldsg§r\"即可添加手持物品到种子白名单，该种子会尝试落地生根(仅对§a方块id§f和§a物品id§c相同§f的作物生效，不区分大小写，注意使用英文的#符号)。"
                },
                {
                    "type": "label",
                    "size": 0.9,
                    "name": "再次在聊天栏输入，可删除该物品的白名单"
                },
                {
                    "type": "label",
                    "size": 0.9,
                    "name": "聊天栏输入\"§l§a#hpldsgmt§r\"添加手持方块为木头，连锁砍树将识别并砍伐；再次输入移除"
                },
                {
                    "name": "gui.saplanting.server.min_wait_time.name",
                    "key": "min_wait_time",
                    "type": "input",
                    "format": "int",
                    "range": [0],
                    "default": MasterSetting.min_wait_time
                },
                {
                    "name": "gui.saplanting.server.tree_felling.name",
                    "key": "tree_felling",
                    "type": "toggle",
                    "default": MasterSetting.tree_felling
                },
                {
                    "name": "gui.saplanting.server.check_leave_persistent_bit.name",
                    "key": "check_leave_persistent_bit",
                    "type": "toggle",
                    "default": MasterSetting.check_leave_persistent_bit
                },
                {
                    "name": "gui.saplanting.server.tree_felling_limit_count.name",
                    "key": "tree_felling_limit_count",
                    "type": "input",
                    "format": "int",
                    "range": [0],
                    "default": MasterSetting.tree_felling_limit_count
                },
                {
                    "name": "gui.saplanting.reset.name",
                    "type": "button",
                    "function": "RESET",
                    "need_confirm": True
                }
            ]
        }
    ]
}
