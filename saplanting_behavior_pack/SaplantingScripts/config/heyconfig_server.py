# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 9:41
# @Author  : taokyla
# @File    : heyconfig_server.py
from .modConfig import MASTER_SETTING_CONFIG_NAME, ModName, ClientSystemName
from .model.server import ServerSavableConfig
from .sapling import default_saplings, LOG_BLOCKS


class MasterSetting(ServerSavableConfig):
    """
    定义并管理服务端的主配置（Master Setting）。
    这些配置由房主（Host）在游戏内修改，并会影响整个服务器的游戏行为。
    """
    _KEY = MASTER_SETTING_CONFIG_NAME

    saplings = default_saplings  # 自动种植的树苗白名单
    min_wait_time = 3  # 树苗落地的最小等待时间（秒）
    tree_felling = True  # 连锁砍树功能总开关
    check_leave_persistent_bit = True  # 连锁砍树时是否检查树叶的persistent_bit，用于区分自然生成树和人工建筑
    tree_felling_limit_count = 255  # 连锁砍树一次最多破坏的方块数
    log_blocks = LOG_BLOCKS  # 被识别为“木头”的方块列表

    def __init__(self):
        """构造函数，初始化默认配置"""
        self.saplings = default_saplings  # type: set[tuple[str, int]]
        self.min_wait_time = 3
        self.tree_felling = True
        self.check_leave_persistent_bit = True
        self.tree_felling_limit_count = 255
        self.log_blocks = LOG_BLOCKS

    def load_data(self, data):
        """
        从字典加载数据来重写配置。
        在加载时，会特殊处理数据格式，例如将列表转换为集合以提高查询效率。
        """
        if "min_wait_time" in data:
            data["min_wait_time"] = max(0, data["min_wait_time"])
        if "saplings" in data:
            data["saplings"] = set(tuple(value) for value in data["saplings"])
        if "log_blocks" in data:
            data["log_blocks"] = set(data["log_blocks"])
        super(MasterSetting, self).load_data(data)

    def dump(self):
        """
        将当前配置导出为字典，用于保存。
        在导出时，会将集合（set）转换为列表（list），因为JSON等格式不支持集合。
        """
        data = super(MasterSetting, self).dump()
        if "saplings" in data:
            data["saplings"] = list(list(value) for value in data["saplings"])
        if "log_blocks" in data:
            data["log_blocks"] = list(data["log_blocks"])
        return data

    def get_client_data(self, add_min_wait_time=True, add_saplings=True):
        """
        获取需要同步给客户端的配置数据。
        出于安全和性能考虑，只会发送客户端必需的数据。
        """
        data = {}
        if add_min_wait_time:
            data["min_wait_time"] = self.min_wait_time
        if add_saplings:
            data["saplings"] = list(list(value) for value in self.saplings)
        return data


# 用于在 HeyConfig 中注册服务端配置的字典结构。
# 定义了只有房主（host）才能修改的设置界面。
register_config_server = {
    "name": "落地生根",
    "mod": ModName,
    "permission": "host",  # 权限声明：只有房主可见
    "categories": [
        {
            "name": "房主设置",
            "key": MASTER_SETTING_CONFIG_NAME,
            "title": "落地生根房主设置",
            "icon": "textures/ui/op",
            "permission": "host",
            "global": True,
            # 回调设置：当房主修改设置后，通知所有客户端去请求更新
            "callback": {
                "function": "CALLBACK",
                "extra": {
                    "name": ModName,
                    "system": ClientSystemName,  # 注意这里是客户端System
                    "function": "reload_master_setting" # 让客户端调用这个方法
                }
            },
            "items": [
                # 以下是GUI中的说明性文本
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
                # 以下是具体的设置项
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
                    "function": "RESET",  # 特殊功能：重置该分类下的所有设置为默认值
                    "need_confirm": True
                }
            ]
        }
    ]
}
