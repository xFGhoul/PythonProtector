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
import humanize
import psutil
import sys

import cpuinfo
import datetime
from pathlib import Path
from threading import Thread
from typing import Dict, Union, List, Tuple, Any, Optional

from command_runner.elevate import is_admin
from loguru import logger

from .constants import ProtectorInfo, LoggingInfo, UserInfo, Valid
from .modules.process import AntiProcess
from .modules.vm import AntiVM
from .modules.dll import AntiDLL
from .modules.miscellaneous import Miscellaneous
from .modules.analysis import AntiAnalysis
from .modules.dump import AntiDump
from .utils.events import ProtectorObservable
from .utils.webhook import Webhook
from .utils.exceptions import ModulesNotValid, DetectionsNotValid, LogsPathEmpty


class PythonProtector:
    def __init__(
        self,
        debug: Optional[bool],
        modules: List[str],
        webhook_url: Optional[str],
        on_detect: Optional[List[str]],
        logs_path: Optional[Union[Path, str]] = None,
    ) -> None:
        """Main PythonProtector Class

        Args:
                debug (bool): Whether Or Not PythonProtector Should Log Actions.
                modules (Set[str]): List Of Modules You Would Like To Enable.
                webhook_url (str): Webhook URL For Reporting Remotely.
                on_detect (Set[str], optional): List of Things PyProtector Does When Detections Are Caused
                logs_path (Union[Path, str]): Path For PythonProtector Logs.

        Raises:
                ModulesNotValid: Raises If Modules Are Not Valid
                DetectionsNotValid: Raises If on_detect parameters are invalid
                LogsPathEmpty: Raises If Debug Is Enabled But No Logs Path Are Provided
        """
        # -- Validate Modules and Detections
        self.modules: List[str] = modules
        _modules_valid: bool = Valid.Modules.issuperset(self.modules)
        if not _modules_valid:
            raise ModulesNotValid(
                "List Of Modules Provided Does Not Match, Consider Checking Valid Modules."
            )

        self.detections: List[str] = on_detect
        _detections_valid: bool = Valid.Detections.issuperset(self.detections)
        if not _detections_valid:
            raise DetectionsNotValid(
                "List Of Detection Methods Don't Match, Consider Checking Valid Detections."
            )

        # -- Initialize Logging
        self.debug: bool | None = debug
        self.logs_path: Path | str | None = logs_path
        self.logger = logger

        if self.debug and not self.logs_path:
            raise LogsPathEmpty("Debug Enabled But No Log Path Was Provided.")

        if self.logs_path and not self.debug:
            raise RuntimeWarning(
                "Logs Path Was Provided But Debug Was Disabled.")

        if self.debug and self.logs_path:
            LOGGING_CONFIG: Dict = {
                "handlers": [
                    {
                        "sink": self.logs_path,
                        "format": LoggingInfo.encrypted_formatter,
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

        # -- Initialize Constants
        self.screenshot: bool = True if "Screenshot" in self.detections else False
        self.exit: bool = True if "Exit" in self.detections else False
        self.report: bool = True if "Report" in self.detections else False

        # -- Initialize Events
        self.event: ProtectorObservable = ProtectorObservable()

        # -- Initialize Webhooks
        self.webhook_url: str = webhook_url

        if self.report and self.webhook_url is None:
            raise RuntimeWarning(
                "Reporting Was Set But No Webhook URL Was Provided.")

        self.webhook: Webhook = Webhook(
            self.webhook_url, self.logs_path, self.screenshot
        )

        # -- Initialize Modules
        self.Miscellaneous: Miscellaneous = Miscellaneous(
            self.webhook, self.logger, self.exit, self.report, self.event
        )
        self.AntiProcess: AntiProcess = AntiProcess(
            self.webhook, self.logger, self.exit, self.report, self.event
        )
        self.AntiDLL: AntiDLL = AntiDLL(
            self.webhook, self.logger, self.exit, self.report, self.event
        )
        self.AntiVM: AntiVM = AntiVM(
            self.webhook, self.logger, self.exit, self.report, self.event
        )
        self.AntiAnalysis: AntiAnalysis = AntiAnalysis(
            self.webhook, self.logger, self.exit, self.report, self.event
        )
        self.AntiDump: AntiDump = AntiDump(
            self.webhook, self.logger, self.exit, self.report, self.event
        )

        # -- Debug Checks
        if self.debug:
            self.logger.enable("PythonProtector")
        else:
            self.logger.disable("PythonProtector")

    @property
    def version(self) -> str:
        """Returns The Current PythonProtector Version

        Returns:
            str: PythonProtector Version
        """
        return ProtectorInfo.VERSION

    @property
    def user(self) -> Tuple[str, str, str]:
        """Returns a Tuple of User Information

        Returns:
            tuple: User Information
        """
        return (UserInfo.PC_NAME, UserInfo.USERNAME, UserInfo.HWID)

    @property
    def ip(self) -> str:
        """Returns The Current IP Address

        Returns:
            str: User's IP Address
        """
        return UserInfo.IP

    @property
    def computer(self) -> Any:
        """Returns The Current Users WMI Computer Object

        Returns:
            Any: Computer Object
        """
        return UserInfo.COMPUTER
    

    def _run_module_threads(self, debug: bool) -> None:
        if debug:
            if "Miscellaneous" in self.modules:
                self.logger.info("Starting Miscellaneous Thread")
                Thread(name=self.Miscellaneous.name,
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
                Thread(
                    name=self.AntiDLL.name,
                    target=self.AntiDLL.BlockDLLs).start()
                self.logger.info("Anti DLL Thread Started")
            if "AntiVM" in self.modules:
                self.logger.info("Starting Anti VM Thread")
                Thread(
                    name=self.AntiVM.name,
                    target=self.AntiVM.StartChecks).start()
                self.logger.info("Anti VM Thread Started")
            if "AntiAnalysis" in self.modules:
                self.logger.info("Starting Anti Analysis Thread")
                Thread(name=self.AntiAnalysis.name,
                       target=self.AntiAnalysis.StartAnalyzing).start()
                self.logger.info("Anti Analysis Thread Started")
            if "AntiDump" in self.modules:
                self.logger.info("Starting Anti Dump Thread")
                Thread(
                    name=self.AntiDump.name, target=self.AntiDump.StartChecks
                ).start()
                self.logger.info("Started Anti Dump Thread")
        else:
            if "Miscellaneous" in self.modules:
                Thread(name=self.Miscellaneous.name,
                       target=self.Miscellaneous.StartChecks).start()
            if "AntiProcess" in self.modules:
                Thread(name="Anti Process List",
                       target=self.AntiProcess.CheckProcessList).start()
                Thread(name="Anti Window Names",
                       target=self.AntiProcess.CheckWindowNames).start()
            if "AntiDLL" in self.modules:
                Thread(
                    name=self.AntiDLL.name,
                    target=self.AntiDLL.BlockDLLs).start()
            if "AntiVM" in self.modules:
                Thread(
                    name=self.AntiVM.name,
                    target=self.AntiVM.StartChecks).start()
            if "AntiAnalysis" in self.modules:
                Thread(name=self.AntiAnalysis.name,
                       target=self.AntiAnalysis.StartAnalyzing).start()
            if "AntiDump" in self.modules:
                Thread(
                    name=self.AntiDump.name, target=self.AntiDump.StartChecks
                ).start()

    def start(self) -> None:
        """Main Function Of PythonProtector

        Raises:
                DeprecationWarning: If Python Version < 3.11
        """
        # -- Check If Windows Platform
        if sys.platform != "win32":
            os._exit(1)

        if platform.python_version_tuple()[1] < "11":
            raise DeprecationWarning("Python Is Not 3.11+")

        # -- Start Main Program
        if self.debug:
            self.logger.info("PythonProtector Starting")

            self.logger.info(f"Version: {ProtectorInfo.VERSION}")
            self.logger.info(f"Current Path: {ProtectorInfo.ROOT_PATH}")
            self.logger.info(
                f"Operating System: {platform.uname().system} {platform.uname().release} {platform.win32_edition()} ({platform.architecture(sys.executable)[0]})"
            )
            bt = datetime.datetime.fromtimestamp(psutil.boot_time())
            self.logger.info(
                f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
            )
            self.logger.info(f"Python: {platform.python_version()}")
            self.logger.info(f"Is Administrator: {is_admin()}")

            cpu_info = cpuinfo.get_cpu_info()
            cpu_type = cpu_info["arch"]
            cpu_cores = cpu_info["count"]

            self.logger.info(f"Processor Type: {cpu_type}")
            self.logger.info(f"Processor Cores: {cpu_cores}")

            vmem = psutil.virtual_memory()

            self.logger.info(
                f"Total Memory: {humanize.naturalsize(vmem.total)}")
            self.logger.info(
                f"Memory Availability: {humanize.naturalsize(vmem.available)}"
            )
            self.logger.info(f"Memory Percentage: {vmem.percent}%")

            self.logger.info("Starting PythonProtector Services")

            self._run_module_threads(debug=True)
        else:
            self._run_module_threads(debug=False)
