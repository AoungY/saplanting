# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod

from .config.modConfig import *


@Mod.Binding(name=ModName, version=ModVersion)
class SaplantingMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def server_init(self):
        serverApi.RegisterSystem(ModName, ServerSystemName, ServerSystemClsPath)

    @Mod.InitClient()
    def client_init(self):
        clientApi.RegisterSystem(ModName, ClientSystemName, ClientSystemClsPath)

    @Mod.DestroyClient()
    def destroy_client(self):
        pass

    @Mod.DestroyServer()
    def destroy_server(self):
        pass
