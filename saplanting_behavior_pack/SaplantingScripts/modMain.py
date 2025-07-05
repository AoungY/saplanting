# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod

from .config.modConfig import *


@Mod.Binding(name=ModName, version=ModVersion)
class SaplantingMod(object):
    """
    模组的主类，用于定义模组的基本信息和初始化流程。
    通过 @Mod.Binding 装饰器将此类与模组名称和版本号绑定。
    """

    def __init__(self):
        """
        类的构造函数，在模组加载时被调用。
        """
        pass

    @Mod.InitServer()
    def server_init(self):
        """
        服务端初始化函数。
        当服务端加载该模组时，此函数会被引擎自动调用。
        主要用于注册服务端的System。
        """
        serverApi.RegisterSystem(ModName, ServerSystemName, ServerSystemClsPath)

    @Mod.InitClient()
    def client_init(self):
        """
        客户端初始化函数。
        当客户端加载该模组时，此函数会被引擎自动调用。
        主要用于注册客户端的System。
        """
        clientApi.RegisterSystem(ModName, ClientSystemName, ClientSystemClsPath)

    @Mod.DestroyClient()
    def destroy_client(self):
        """
        客户端销毁函数。
        当客户端退出或卸载模组时，此函数会被引擎调用。
        可用于清理客户端资源。
        """
        pass

    @Mod.DestroyServer()
    def destroy_server(self):
        """
        服务端销毁函数。
        当服务端关闭或卸载模组时，此函数会被引擎调用。
        可用于清理服务端资源或保存数据。
        """
        pass
