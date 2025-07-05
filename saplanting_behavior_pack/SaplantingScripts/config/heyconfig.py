# -*- coding: utf-8 -*-
# @Time    : 2023/12/8 14:28
# @Author  : taokyla
# @File    : heyconfig.py
from .modConfig import CLIENT_SETTING_CONFIG_NAME, ModName, ClientSystemName
from .model.client import ClientSavableConfig


class ClientSetting(ClientSavableConfig):
    _KEY = CLIENT_SETTING_CONFIG_NAME
    _ISGLOBAL = True

    tree_felling = True

    def __init__(self):
        self.tree_felling = True


register_config = {
    "name": "落地生根",
    "mod": ModName,
    "categories": [
        {
            "name": "客户端设置",
            "key": CLIENT_SETTING_CONFIG_NAME,
            "title": "落地生根客户端设置",
            "icon": "textures/ui/anvil_icon",
            "global": True,
            "callback": {
                "function": "CALLBACK",
                "extra": {
                    "name": ModName,
                    "system": ClientSystemName,
                    "function": "reload_client_setting"
                }
            },
            "items": [
                {
                    "name": "gui.quick_suit.client.tree_felling.name",
                    "key": "tree_felling",
                    "type": "toggle",
                    "default": ClientSetting.tree_felling
                }
            ]
        }
    ]
}
