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

import cpuinfo
from pathlib import Path
from threading import Thread
from typing import Dict, Union, List, Optional

from command_runner.elevate import is_admin
from loguru import logger

from .constants import ProtectorInfo, Valid
from .modules.process import AntiProcess
from .modules.vm import AntiVM
from .modules.dll import AntiDLL
from .modules.miscellaneous import Miscellaneous
from .utils.exceptions import ModulesNotValid, LogsPathEmpty


class PythonProtector:
    def __init__(self, debug: Optional[bool], modules: List[str], logs_path: Optional[Union[Path, str]], webhook_url: str, should_exit: bool = True) -> None:
        """Main PythonProtector Class

        Args:
            debug (bool): Whether Or Not PythonProtector Should Log Actions.
            modules (List[str]): List Of Modules You Would Like To Enable.
            logs_path (Union[Path, str]): Path For PythonProtector Logs.
            webhook_url (str): Webhook URL For Reporting Remotely.
            should_exit (bool, optional): Whether The Program Should Exit. Defaults to True.

        Raises:
            ModulesNotValid: Raises If Modules Are Not Valid
            LogsPathEmpty: Raises If Debug Is Enabled But No Logs Path Are Provided
        """
        
        self.modules = modules
        _modules_valid = Valid.Modules.issuperset(self.modules)
        if _modules_valid != True:
            raise ModulesNotValid("List Of Modules Provided Does Not Match, Consider Checking Valid Modules.")
        
        # -- Initialize Logging
        self.debug = debug
        self.logs_path = logs_path
        self.logger = logger
        
        if self.debug and not self.logs_path:
            raise LogsPathEmpty("Debug Enabled But No Log Path Was Provided.")
        
        if self.logs_path and not self.debug:
            raise RuntimeWarning("Logs Path Was Provided But Debug Was Disabled.")

        LOGGING_CONFIG: Dict = {
            "handlers": [
                {
                    "sink": self.logs_path,
                    "format": "[{time:YYYY-MM-DD HH:mm:ss}] {module}::{function}({line}) - {message}",
                    "enqueue": True,
                    "rotation": "daily",
                    "mode": "w",
                    "level": "INFO",
                    "serialize": False,
                    "backtrace": False,
                    "catch": False,
                },
            ],
        }
        self.logger.configure(**LOGGING_CONFIG)

        # -- Initialize Webhooks
        self.webhook_url = webhook_url
        
        # -- Initialize Constants
        self.should_exit = should_exit

        # -- Initialize Modules
        self.Miscellaneous = Miscellaneous(self.webhook_url, self.logger, self.should_exit)
        self.AntiProcess = AntiProcess(self.webhook_url, self.logger, self.should_exit)
        self.AntiDLL = AntiDLL(self.webhook_url, self.logger, self.should_exit)
        self.AntiVM = AntiVM(self.webhook_url, self.logger, self.should_exit)

        # -- Debug Checks
        if self.debug:
            self.logger.enable("PythonProtector")
        else:
            self.logger.disable("PythonProtector")
            
    def run_module_threads(self, debug: bool) -> None:
        if debug == True:
            if "Miscellaneous" in self.modules:
                self.logger.info("Starting Miscellaneous Thread")
                Thread(
                    name="Miscellaneous",
                    target=self.Miscellaneous.StartChecks).start()
                self.logger.info("Miscellaneous Thread Started")
            if "AntiProcess" in self.modules:
                self.logger.info("Starting Anti Process Thread")
                Thread(name="Anti Process List",
                   target=self.AntiProcess.CheckProcessList).start()
                Thread(name="Anti Window Names",
                   target=self.AntiProcess.CheckWindowNames).start()
                self.logger.info("Anti Process Thread Started")
            if "AntiDLL" in self.modules:
                self.logger.info("Starting Anti DLL Thread")
                Thread(name="Anti DLL", target=self.AntiDLL.BlockDLLs).start()
                self.logger.info("Anti DLL Thread Started")
            if "AntiVM" in self.modules:
                self.logger.info("Starting Anti VM Thread")
                Thread(name="Anti VM", target=self.AntiVM.StartChecks).start()
                self.logger.info("Anti VM Thread Started")
        else:
            if "Miscellaneous" in self.modules:
                Thread(
                    name="Miscellaneous",
                    target=self.Miscellaneous.StartChecks).start()
            if "AntiProcess" in self.modules:
                Thread(name="Anti Process List",
                    target=self.AntiProcess.CheckProcessList).start()
                Thread(name="Anti Window Names",
                    target=self.AntiProcess.CheckWindowNames).start()
            if "AntiDLL" in self.modules:
                Thread(name="Anti DLL", target=self.AntiDLL.BlockDLLs).start()
            if "AntiVM" in self.modules:
                Thread(name="Anti VM", target=self.AntiVM.StartChecks).start()
            

    def start(self) -> None:
        # -- Check If Windows Platform
        if sys.platform != "win32":
            os._exit(1)

        if platform.python_version_tuple()[1] < "10":
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
            self.logger.info(f"Is Administrator: {is_admin()}")

            cpu_info = cpuinfo.get_cpu_info()
            cpu_type = cpu_info["arch"]
            cpu_cores = cpu_info["count"]

            self.logger.info(f"Processor Type: {cpu_type}")
            self.logger.info(f"Processor Cores: {cpu_cores}")

            self.logger.info("Starting Services")

            self.run_module_threads(debug=True)
        else:
            self.run_module_threads(debug=False)
