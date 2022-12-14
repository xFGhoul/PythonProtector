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
import socket
import struct
import requests
import psutil
import win32api

from typing import Literal, Any

from ..constants import Lists, UserInfo, Lists
from ..utils.http import hasInternet
from ..utils.webhook import Webhook


class Miscellaneous:
    def __init__(
            self,
            webhook: Webhook,
            logger: Any,
            exit: bool,
            report: bool) -> None:
        self.webhook: Webhook = webhook
        self.logger = logger
        self.exit: bool = exit
        self.report: bool = report

    def CheckInternet(self) -> None:
        while True:
            try:
                time.sleep(5)
                if hasInternet() == False:
                    self.logger.info("CheckInternet Failed")
                    if self.exit:
                        os._exit(1)
                else:
                    pass
            except BaseException:
                pass

    def CheckRam(self) -> None:
        memory: int = psutil.virtual_memory().total
        if memory <= 4294967296:
            self.logger.info("RAM Check Failed")
            if self.report:
                self.webhook.send(
                    f"RAM Check: Less than 4 GB of RAM exists on this system",
                    "Miscellaneous",
                )
            if self.exit:
                os._exit(1)

    def CheckIsDebuggerPresent(self) -> None:
        isDebuggerPresent = ctypes.windll.kernel32.IsDebuggerPresent()

        if isDebuggerPresent:
            self.logger.send("IsDebuggerPresent Returned True")
            if self.report:
                self.webhook.send(
                    f"IsDebuggerPresent: A debugger is present, exiting program...",
                    "Miscellaneous",
                )
            if self.exit:
                os._exit(1)

        if (
            ctypes.windll.kernel32.CheckRemoteDebuggerPresent(
                ctypes.windll.kernel32.GetCurrentProcess(), False
            )
            != 0
        ):
            self.logger.send("CheckRemoteDebuggerPresent Returned True")
            if self.report:
                self.webhook.send(
                    "CheckRemoteDebuggerPresent: A debugger is present, exiting program...",
                    "Miscellaneous",
                )
            if self.exit:
                os._exit(1)

    def CheckDiskSize(self) -> None:
        minDiskSizeGB: Literal[50] = 50
        if len(sys.argv) > 1:
            minDiskSizeGB = float(sys.argv[1])
        _, diskSizeBytes, _ = win32api.GetDiskFreeSpaceEx()
        diskSizeGB = diskSizeBytes / 1073741824

        if diskSizeGB < minDiskSizeGB:
            self.logger.info("Disk Check Failed")
            if self.report:
                self.webhook.send(
                    f"Disk Check: The disk size of this host is {diskSizeGB} GB, which is less than the minimum {minDiskSizeGB} GB"
                )
            if self.exit:
                os._exit(1)

    def KillTasks(self) -> None:
        self.logger.info("Killing Tasks")
        os.system("taskkill /f /im HTTPDebuggerUI.exe >nul 2>&1")
        os.system("taskkill /f /im HTTPDebuggerSvc.exe >nul 2>&1")
        os.system("sc stop HTTPDebuggerPro >nul 2>&1")
        os.system(
            'cmd.exe /c @RD /S /Q "C:\\Users\\%username%\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE" >nul 2>&1'
        )
        self.logger.info("All Tasks Killed")

    def CheckPaths(self) -> None:
        for path in Lists.BLACKLISTED_PATHS:
            if os.path.exists(path):
                self.logger.info("Blacklisted Path Found")
                if self.report:
                    self.webhook.send(
                        "Blacklisted Path Found", "Miscellaneous")
                if self.exit:
                    os._exit(1)
            else:
                pass

    def CheckImports(self) -> None:
        for package in Lists.BLACKLISTED_IMPORTS:
            try:
                dist = pkg_resources.get_distribution(package)
                if dist:
                    self.logger.info(f"{package} Was Found Installed")
                    if self.report:
                        self.webhook.send(
                            f"`{package}` Was Found Installed On User Machine",
                            "Miscellaneous",
                        )
                    if self.exit:
                        os._exit(1)
                else:
                    pass
            except pkg_resources.DistributionNotFound:
                pass

    def CheckOutPutDebugString(self) -> None:
        win32api.SetLastError(0)
        win32api.OutputDebugString("PythonProtector Intruding...")
        if win32api.GetLastError() != 0:
            self.logger.info("OutputDebugString Is Not 0")
            if self.report:
                self.webhook.send(
                    "OutputDebugString Not Equal To 0",
                    "Miscellaneous")
            if self.exit:
                os._exit(1)

    def CheckIPs(self) -> None:
        if UserInfo.IP in Lists.BLACKLISTED_IPS:
            self.logger.info(f"{UserInfo.IP} Is A Blacklisted IP Address")
            if self.report:
                self.webhook.send(
                    f"`{UserInfo.IP}` Is A Blacklisted IP Address",
                    "Miscellaneous")
            if self.exit:
                os._exit(1)
        else:
            pass

    def CheckCPUCores(self) -> None:
        if int(psutil.cpu_count()) <= 1:
            self.logger.info(f"CPU Core Count Is Less Than Or Equal To 1")
            if self.report:
                self.webhook.send(
                    f"CPU Core Count Is Less Than Or Equal To `1`",
                    "Miscellaneous")
            if self.exit:
                os._exit(1)

    def IsUsingProxy(self) -> None:
        headers: dict[str, str] = {"User-Agent": "Mozilla/5.0"}
        response = requests.get("https://www.google.com", headers=headers)
        for header in Lists.PROXY_HEADERS:
            if header in response.headers:
                self.logger.info("Proxy Headers In Use")
                if self.report:
                    self.webhook.send(
                        "Proxy Headers Being Used", "Miscellaneous")
                if self.exit:
                    os._exit(1)

        if UserInfo.IP in Lists.PROXY_IPS:
            self.logger.info("Proxy IP In Use")
            if self.report:
                self.webhook.send("Proxy IP Being Used", "Miscellaneous")
            if self.exit:
                os._exit(1)

        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.settimeout(5)
            _socket.connect(("check.torproject.org", 9050))
            _socket.send(
                b"GET / HTTP/1.1\r\nHost: check.torproject.org\r\n\r\n")
            data: bytes = _socket.recv(1024)
            if "Congratulations" in data.decode():
                self.logger.info("Tor Network Detected")
                if self.report:
                    self.webhook.send("Tor Network In Use", "Miscellaneous")
                if self.exit:
                    os._exit(1)
        except Exception:
            pass

        try:
            IP = struct.unpack("!I", socket.inet_aton(UserInfo.IP))[0]
            if IP >> 24 in [0, 10, 100, 127, 169, 172, 192]:
                self.logger.info("Transparent Proxies Detected")
                if self.report:
                    self.webhook.send(
                        "Transparent Proxies Detected", "Miscellaneous")
                if self.exit:
                    os._exit(1)
        except Exception:
            pass

    def StartChecks(self) -> None:
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
        self.IsUsingProxy()

        self.CheckInternet()
