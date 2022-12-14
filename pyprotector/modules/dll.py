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
import time

import win32api
import win32process

from typing import Any

from ..constants import Lists
from ..utils.webhook import Webhook


class AntiDLL:
    def __init__(
            self,
            webhook: Webhook,
            logger: Any,
            exit: bool,
            report: bool) -> None:
        self.webhook: Webhook = webhook
        self.logger: Any = logger
        self.exit: bool = exit
        self.report: bool = report

    def BlockDLLs(self) -> None:
        while True:
            try:
                time.sleep(1)
                EvidenceOfSandbox = []
                allPids: tuple = win32process.EnumProcesses()
                for pid in allPids:
                    try:
                        hProcess: int = win32api.OpenProcess(0x0410, 0, pid)
                        try:
                            curProcessDLLs: tuple = win32process.EnumProcessModules(
                                hProcess)
                            for dll in curProcessDLLs:
                                dllName: str = str(
                                    win32process.GetModuleFileNameEx(
                                        hProcess, dll)).lower()
                                for sandboxDLL in Lists.BLACKLISTED_DLLS:
                                    if sandboxDLL in dllName:
                                        if dllName not in EvidenceOfSandbox:
                                            EvidenceOfSandbox.append(dllName)
                        finally:
                            win32api.CloseHandle(hProcess)
                    except BaseException:
                        pass
                if EvidenceOfSandbox:
                    self.logger.info(
                        f"The Following DLL's: {EvidenceOfSandbox} Were Found Loaded"
                    )
                    if self.report:
                        self.webhook.send(
                            f"The following sandbox-indicative DLLs were discovered loaded in processes running on the system. DLLS: {EvidenceOfSandbox}",
                            "Anti DLL",
                        )
                    if self.exit:
                        os._exit(1)
            except BaseException:
                pass
