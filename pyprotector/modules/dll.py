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

from ..constants import Lists
from ..utils.webhook import Webhook


class AntiDLL:
    def __init__(self, webhook_url: str, logger, should_exit):
        self.webhook_url = webhook_url
        self.logger = logger
        self.webhook = Webhook(self.webhook_url)
        self.should_exit = should_exit

    def BlockDLLs(self) -> None:
        while True:
            try:
                time.sleep(1)
                EvidenceOfSandbox = []
                allPids = win32process.EnumProcesses()
                for pid in allPids:
                    try:
                        hProcess = win32api.OpenProcess(0x0410, 0, pid)
                        try:
                            curProcessDLLs = win32process.EnumProcessModules(
                                hProcess)
                            for dll in curProcessDLLs:
                                dllName = str(
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
                    self.webhook.send(
                        f"The following sandbox-indicative DLLs were discovered loaded in processes running on the system. DLLS: {EvidenceOfSandbox}",
                        "Anti DLL",
                    )
                    if self.should_exit:
                        os._exit(1)
            except BaseException:
                pass
