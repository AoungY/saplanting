# -*- coding: utf-8 -*-

# Mod Info
ModName = "Saplanting"
"""模组的内部名称，用于注册系统和事件"""
ModVersion = "0.0.1"
"""模组的版本号"""
TeamName = "HeyPixel"
"""团队或作者的名称，用于构成独立的配置名称以避免冲突"""

# Server System
ServerSystemName = ModName + "ServerSystem"
"""服务端System的名称"""
ServerSystemClsPath = "SaplantingScripts.server." + ModName + "Server." + ModName + "Server"
"""服务端System主类的完整路径，用于引擎动态加载"""

# Client System
ClientSystemName = ModName + "ClientSystem"
"""客户端System的名称"""
ClientSystemClsPath = "SaplantingScripts.client." + ModName + "Client." + ModName + "Client"
"""客户端System主类的完整路径，用于引擎动态加载"""

RootDir = "SaplantingScripts"
"""脚本的根目录名称"""
# Engine
Minecraft = "Minecraft"
"""原生Minecraft的命名空间"""

CLIENT_SETTING_CONFIG_NAME = TeamName + ModName + "ClientSetting"
"""客户端配置文件名或键名"""
MASTER_SETTING_CONFIG_NAME = TeamName + ModName + "MasterSetting"
"""服务端主配置文件名或键名"""
