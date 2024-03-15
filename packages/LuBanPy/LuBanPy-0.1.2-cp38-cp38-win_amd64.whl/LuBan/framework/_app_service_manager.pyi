#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_app_service_manager.py
@Author     ：Alex
@Date       ：2024/2/26 10:52 
@Function   ：应用服务管理器
"""
from .support import (
    ConfigSupport,
    HookSupport,
    GlobalShareVarsSupport,
    ProcessServiceSupport,
    IPCSupport
)




class __AppServiceManager(
        IPCSupport,
        ProcessServiceSupport,
        GlobalShareVarsSupport,
        HookSupport,
        ConfigSupport):

    def __init__(self):
        """
        初始化函数
        """
        pass

    @property
    def isDebug(self) -> bool:
        pass

    @property
    def isProduction(self) -> bool:
        pass

    def run(self, loop: bool = True):
        """
        应用服务管理器运行正在启动入口

        :param bool loop:       是否启用主系统消息
        :return:
        """
        pass

    def exit(self):
        """
        退出应用操作(推送请求)
        :return:
        """
        pass

    @property
    def isExit(self) -> bool:
        """当前是否已标记退出"""
        pass

    def command(self, directive: str, params=None):
        """
        发送命令
        :param directive:
        :param params:
        :return:
        """
        pass


App = __AppServiceManager()

__all__ = ['App']


