"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
       /____/

Made With ❤️ By Ghoul & Marci
"""

import os
import platform
import sys
from pathlib import Path
from threading import Thread
from typing import Dict, Union

import cpuinfo
from command_runner.elevate import is_admin
from loguru import logger

from .constants import ProtectorInfo
from .modules.antiprocess import AntiProcess
from .modules.antivm import AntiVM
from .modules.dll import AntiDLL
from .modules.miscellaneous import Miscellanoeus
from .utils.webhook import Webhook


class PythonProtector:
    def __init__(self,
                 debug: bool,
                 logs_path: Union[Path,
                                  str],
                 webhook_url: str):
        # -- Intialize Logging
        self.debug = debug
        self.logs_path = logs_path

        LOGGING_CONFIG: Dict = {
            "handlers": [
                {
                    "sink": self.logs_path,
                    "format": "[{time:YYYY-MM-DD HH:mm:ss}] {module}::{function}({line}) - {message}",
                    "enqueue": True,
                    "rotation": "daily",
                    "level": "INFO",
                    "serialize": False,
                    "backtrace": False,
                    "catch": False,
                },
            ],
        }
        logger.configure(**LOGGING_CONFIG)

        # -- Initialize Webhooks
        self.webhook_url = webhook_url
        self.webhook = Webhook(self.webhook_url)

        # -- Naming Convention
        self.logger = logger

        # -- Initialize Modules
        self.misceallneous = Miscellanoeus(self.webhook_url, self.logger)
        self.anti_process = AntiProcess(self.webhook_url, self.logger)
        self.anti_dll = AntiDLL(self.webhook_url, self.logger)
        self.anti_vm = AntiVM(self.webhook_url, self.logger)

        # -- Debug Checks
        if self.debug:
            self.logger.enable("PythonProtector")
        else:
            self.logger.disable("PythonProtecttor")

    def start(self):
        # -- Check If Windows Platform
        if sys.platform != "win32":
            os._exit(1)

        if platform.python_version_tuple()[1] != "10":
            raise DeprecationWarning("Python Is Not 3.10+")

        # -- Start Main Program
        if self.debug:
            self.logger.info("PythonProtector Starting")

            self.logger.info(f"Version: {ProtectorInfo.VERSION}")
            self.logger.info(f"Current Path: {ProtectorInfo.ROOT_PATH}")
            self.logger.info(
                f"Operating System: {platform.uname().system} {platform.uname().release} {platform.win32_edition()} ({platform.architecture(sys.executable)[0]})"
            )
            self.logger.info(f"Python: {platform.python_version()}")
            self.logger.info(f"Is Administrtor: {is_admin()}")

            cpu_info = cpuinfo.get_cpu_info()
            cpu_type = cpu_info["arch"]
            cpu_cores = cpu_info["count"]

            self.logger.info(f"Processer Type: {cpu_type}")
            self.logger.info(f"Processer Cores: {cpu_cores}")

            self.logger.info("Starting Services")

            self.logger.info("Starting Miscellaneous Thread")
            Thread(
                name="Miscellaneous",
                target=self.misceallneous.StartChecks).start()
            self.logger.info("Miscellaneous Thread Started")

            self.logger.info("Starting Anti Process Thread")
            Thread(name="Anti Process List",
                   target=self.anti_process.CheckProcessList).start()
            Thread(name="Anti Window Names",
                   target=self.anti_process.CheckWindowNames).start()
            self.logger.info("Anti Process Thread Started")

            self.logger.info("Starting Anti DLL Thread")
            Thread(name="Anti DLL", target=self.anti_dll.BlockDLLs).start()
            self.logger.info("Anti DLL Thread Started")

            self.logger.info("Starting Anti VM Thread")
            Thread(name="Anti VM", target=self.anti_vm.StartChecks).start()
            self.logger.info("Anti VM Thread Started")
        else:
            Thread(
                name="Miscellaneous",
                target=self.misceallneous.StartChecks).start()
            Thread(name="Anti Process List",
                   target=self.anti_process.CheckProcessList).start()
            Thread(name="Anti Window Names",
                   target=self.anti_process.CheckWindowNames).start()
            Thread(name="Anti DLL", target=self.anti_dll.BlockDLLs).start()
            Thread(name="Anti VM", target=self.anti_vm.StartChecks).start()
