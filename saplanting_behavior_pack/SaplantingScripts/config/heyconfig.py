# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 14:28
# @Author  : taokyla
# @File    : heyconfig.py
from .modConfig import CLIENT_SETTING_CONFIG_NAME, ModName, ClientSystemName
from .model.client import ClientSavableConfig


class ClientSetting(ClientSavableConfig):
    """
    定义并管理客户端的本地设置。
    这些设置通常由玩家自己在游戏内修改，并且只影响该玩家的客户端。
    """
    _KEY = CLIENT_SETTING_CONFIG_NAME
    _ISGLOBAL = True

    # 连锁砍树功能的开关，默认为开启
    tree_felling = True

    def __init__(self):
        """构造函数，初始化默认设置值"""
        self.tree_felling = True


# 这是一个用于注册到 HeyConfig 配置系统的字典结构。
# 它详细描述了模组的设置在游戏内GUI中的显示方式和行为。
register_config = {
    "name": "落地生根",  # 配置界面的模组名称
    "mod": ModName,
    "categories": [
        {
            "name": "客户端设置",
            "key": CLIENT_SETTING_CONFIG_NAME,
            "title": "落地生根客户端设置",  # 分类标题
            "icon": "textures/ui/anvil_icon",  # 分类图标
            "global": True,  # 是否为全局设置
            # 当设置被修改时，会调用此回调函数
            "callback": {
                "function": "CALLBACK",
                "extra": {
                    "name": ModName,
                    "system": ClientSystemName,
                    "function": "reload_client_setting"  # 具体调用的客户端System中的方法
                }
            },
            # 定义该分类下的具体设置项
            "items": [
                {
                    "name": "gui.quick_suit.client.tree_felling.name",  # 设置项的名称，这是一个语言文件中的key
                    "key": "tree_felling",  # 对应 ClientSetting 类中的属性名
                    "type": "toggle",  # GUI控件类型：开关
                    "default": ClientSetting.tree_felling  # 默认值
                }
            ]
        }
    ]
}
