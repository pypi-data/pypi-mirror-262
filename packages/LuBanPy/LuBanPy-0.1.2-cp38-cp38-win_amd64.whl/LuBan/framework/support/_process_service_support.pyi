#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@Project    ：LuBanPy 
@File       ：_process_service_support.py
@Author     ：Alex
@Date       ：2024/2/27 18:40 
@Function   ：进程服务扩展支持工具
"""
import multiprocessing
import os
import pprint
import time
import traceback

from loguru import logger
from typing import Dict, Any, Optional, List
from .._app_service_container import AppServiceContainer


class ProcessServiceSupport:

    def start(self, cls: str, params: Optional[dict] = None, name: Optional[str] = None, daemon: bool = False, worker: int = 1, sync: bool = False):
        """
        启动新的服务进程发送指令

        :param str cls:                         应用服务类名，需要实现`AppServiceInterface`接口
        :param Optional[dict] params:           可以给应用服务类传递参数
        :param Optional[str] name:              指定应用服务的名称，未指定时使用类名
        :param bool daemon:                     是守护进程
        :param int worker:                      指定服务启动的子进程数量，最少必须为1
        :param sync sync:                       是否使用同步(True)或异步(False)模式启动进程（异步无需等待进程启动完成，即可调用下一进程启动）
        :return:
        """
        pass
